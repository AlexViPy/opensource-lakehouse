from pyspark.sql import SparkSession
from sparksession import spark_session


spark = spark_session(SparkSession, "created hive schems")

spark.sql(f"DROP SCHEMA IF EXISTS bronze")
spark.sql(f"DROP SCHEMA IF EXISTS silver")
spark.sql(f"DROP SCHEMA IF EXISTS gold")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS bronze")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS silver")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS gold")
spark.sql("SHOW DATABASES").show()
