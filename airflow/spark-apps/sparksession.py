import os

AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
AWS_S3_ENDPOINT = "http://minio:9000"
AWS_BUCKET_NAME = "data-platform-core"
EXTRA_CLASS_PATH_JARS = "".join([
    "/opt/bitnami/spark/jars/aws-java-sdk-1.12.367.jar",
    "/opt/bitnami/spark/jars/delta-core_2.12-2.2.0.jar",
    "/opt/bitnami/spark/jars/delta-storage-2.2.0.jar",
    "/opt/bitnami/spark/jars/postgresql-42.7.4.jar",
    "/opt/bitnami/spark/jars/s3-2.18.41.jar",
])


def spark_session(spark_session, app_name):

    spark = spark_session.builder \
        .appName(app_name) \
        .master('spark://spark-master:7077') \
        .config("hive.metastore.uris", "thrift://hive-metastore:9083")\
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.endpoint", AWS_S3_ENDPOINT)\
        .config("spark.hadoop.fs.s3a.path.style.access", "true")\
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")\
        .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
        .config('spark.sql.warehouse.dir', f's3a://{AWS_BUCKET_NAME}/')\
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.4')\
        .config('spark.driver.extraClassPath', f'/opt/bitnami/spark/jars/hadoop-aws-3.3.4.jar:{EXTRA_CLASS_PATH_JARS}')\
        .config('spark.executor.extraClassPath', f'/opt/bitnami/spark/jars/hadoop-aws-3.3.4.jar:{EXTRA_CLASS_PATH_JARS}')\
        .enableHiveSupport()\
        .getOrCreate()

    spark.sparkContext.setLogLevel("INFO")

    return spark