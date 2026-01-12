# api_client.py
import requests
import pandas as pd
import duckdb

FASTAPI_BASE_URL = "http://127.0.0.1:8000"  # 部署到 Render 后改成公开地址

def fetch_parquet_from_gcs(gcs_path: str) -> pd.DataFrame:
    """
    通过 DuckDB 读取 GCS 上 Parquet 文件
    """
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    query = f"SELECT * FROM read_parquet('{gcs_path}')"
    df = con.execute(query).df()
    return df
