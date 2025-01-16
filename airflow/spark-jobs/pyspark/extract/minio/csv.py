import ast
import sys
from datetime import datetime, timedelta
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
PARTITION_BY = _params.get("partition_by")

ts = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

# init pyspark.Session
spark = SparkSession.builder.appName(f"ETL: minio/hive: {HIVE_DB}.{HIVE_TABLE}").enableHiveSupport().getOrCreate()
spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DB}")

df = spark.read.option("header", True).csv(OUTPUT_PATH)
if PARTITION_BY:
    df.write.partitionBy(PARTITION_BY).saveAsTable(
        f"{HIVE_CTLG}.{HIVE_DB}.{HIVE_TABLE}", path=SAVE_PATH, mode=MODE, format="iceberg"
    )
else:
    df.write.saveAsTable(
        f"{HIVE_CTLG}.{HIVE_DB}.{HIVE_TABLE}", path=SAVE_PATH, mode=MODE, format="iceberg"
    )


spark.sql(
    f"""
    CALL {HIVE_CTLG}.system.rewrite_data_files(
        table => '{HIVE_DB}.{HIVE_TABLE}', 
        strategy => 'binpack', 
        options => map('target-file-size-bytes', {1024 * 1024 * 100})
    )
    """
)


spark.sql(
    f"""
    CALL {HIVE_CTLG}.system.expire_snapshots(
        table => '{HIVE_DB}.{HIVE_TABLE}', 
        older_than => TIMESTAMP '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 
        retain_last => 1
    )
    """
)

spark.sql(
    f"""
    CALL {HIVE_CTLG}.system.remove_orphan_files(
        table => '{HIVE_DB}.{HIVE_TABLE}', 
        older_than => TIMESTAMP '{ts}'
    )
    """
)

spark.sql(
    f"""
    CALL {HIVE_CTLG}.system.rewrite_manifests(
        table => '{HIVE_DB}.{HIVE_TABLE}'
    )
    """
)