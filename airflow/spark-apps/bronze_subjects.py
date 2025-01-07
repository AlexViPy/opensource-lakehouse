from pyspark.sql import SparkSession
from sparksession import spark_session


spark = spark_session(SparkSession, "load bronze.subjects")

df = spark.read.option("header", "true").csv("s3a://raw-data/csv/dict__zunami__subjects.csv")
df.write.format("delta").mode("overwrite").saveAsTable("bronze.subjects")
spark.sql("SHOW TABLES IN bronze").show()