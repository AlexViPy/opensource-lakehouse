import os
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Default arguments for the DAG
DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
}
DAG_ID = "BRONZE__MINIO__GAMES_FIFA"
EXTRA_CLASS_PATH_JARS = ",".join(
    os.path.join("/opt/airflow/jars", p) for p in os.listdir("/opt/airflow/jars")
)


# Define the DAG
with DAG(
    dag_id=DAG_ID,
    default_args=DEFAULT_ARGS,
    description="Load data to bronze layer using SparkSubmitOperator",
    schedule_interval=None,
    catchup=False,
) as dag:
    # Define the SparkSubmitOperator
    export_minio_task = SparkSubmitOperator(
        task_id=f"export__{DAG_ID.lower()}",
        application="/opt/airflow/spark-jobs/pyspark/extract/minio/csv.py",
        packages="org.apache.hadoop:hadoop-aws:3.3.4",
        jars=EXTRA_CLASS_PATH_JARS,
        conn_id="spark-master",
        conf={
            "spark.sql.extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkCatalog",
            "spark.sql.catalog.spark_catalog.type": "hive",
            "spark.sql.catalog.spark_catalog.uri": "thrift://hive-metastore:9083",
            "spark.sql.catalog.spark_catalog.warehouse": "s3a://data-platform-core/",
            "spark.sql.warehouse.dir": "s3a://data-platform-core/",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": os.getenv("AWS_ACCESS_KEY_ID"),
            "spark.hadoop.fs.s3a.secret.key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        },
        application_args=[
            str(
                {
                    "save_path": "s3a://data-platform-core/bronze/fifa",
                    "output_path": "s3a://raw-data/csv/games/fifa",
                    "strategy": "overwrite",
                    "hive_ctlg": "spark_catalog",
                    "hive_db": "bronze",
                    "hive_table": "fifa",
                    "partition_by": "Team",
                }
            )
        ],
        verbose=True,
        dag=dag,
    )
