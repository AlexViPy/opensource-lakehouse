from datetime import timedelta, datetime

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2023, 7, 1),
    'retries': 0,
    'schedule_interval': '15 08 * * *',
    'retry_delay': timedelta(seconds=5),
    'dagrun_timeout': timedelta(hours=12),
}

EXTRA_CLASS_PATH_JARS = ",".join([
    "/opt/airflow/jars/aws-java-sdk-1.12.367.jar",
    "/opt/airflow/jars/delta-core_2.12-2.2.0.jar",
    "/opt/airflow/jars/delta-storage-2.2.0.jar",
    "/opt/airflow/jars/hadoop-aws-3.3.4.jar",
    "/opt/airflow/jars/postgresql-42.7.4.jar",
    "/opt/airflow/jars/s3-2.18.41.jar",
])

EXTRA_CLASS_PATH_PACKAGES = ",".join([
    "com.amazonaws:aws-java-sdk:1.12.367",
    "io.delta:delta-spark_2.12:2.3.0",
    "io.delta:delta-storage:2.3.0",
    "org.apache.hadoop:hadoop-aws:3.3.4",
    "software.amazon.awssdk:s3:2.18.41",
])



with DAG(
    'etl_pipeline', 
    default_args=default_args,  
    schedule_interval=None
) as dag:
    create_schema = SparkSubmitOperator(
        task_id='create_schema',
        total_executor_cores='1',
        executor_cores='1',
        executor_memory='1g',
        num_executors='1',
        driver_memory='1g',
        application="../airflow/spark-apps/create_schema.py",
        packages="org.apache.hadoop:hadoop-aws:3.3.4",
        jars=EXTRA_CLASS_PATH_JARS,
        conn_id="spark-master" , # Connection ID for your Spark cluster configuration
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        },
        verbose=True
        
    )

    ingest_subjects = SparkSubmitOperator(
        task_id='ingest_subjects',
        total_executor_cores='1',
        executor_cores='1',
        executor_memory='2g',
        num_executors='1',
        driver_memory='2g',
        application="/opt/airflow/spark-apps/bronze_subjects.py",
        packages="org.apache.hadoop:hadoop-aws:3.3.4",
        jars=EXTRA_CLASS_PATH_JARS,
        conn_id="spark-master" , # Connection ID for your Spark cluster configuration
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        }
    )

create_schema >> ingest_subjects