import ast
import sys
from pyspark.sql import SparkSession

# required vars
_params = ast.literal_eval(sys.argv[1:][-1])

SAVE_PATH = _params.get("save_path")
OUTPUT_PATH = _params.get("output_path")
STRATEGY = _params.get("strategy")
MODE = "append" if STRATEGY == "increment" else "overwrite"
HIVE_CTLG = _params.get("hive_ctlg")
HIVE_DB = _params.get("hive_db")
HIVE_TABLE = _params.get("hive_table")

# init pyspark.Session
spark = SparkSession.builder.appName(f"ETL: minio/hive: {HIVE_DB}.{HIVE_TABLE}").enableHiveSupport().getOrCreate()
spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DB}")

df = spark.read.option("header", True).csv(OUTPUT_PATH)
df.write.saveAsTable(f"{HIVE_CTLG}.{HIVE_DB}.{HIVE_TABLE}", path=SAVE_PATH, mode=MODE, format="iceberg")