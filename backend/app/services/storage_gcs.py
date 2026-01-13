from google.cloud import bigquery
from google.oauth2 import service_account
from app.setting import get_settings
from dotenv import load_dotenv
import datetime
from datetime import date
import uuid

load_dotenv()

rows = []

def get_bigquery_client():
    s = get_settings()
    credentials = service_account.Credentials.from_service_account_info(
        s.BIGQUERY_CREDENTIALS
    )
    client = bigquery.Client(
        project=s.GCP_PROJECT_ID,
        credentials=credentials
    )
    return client

    # return bigquery.Client.from_service_account_json(
    #     str(s.BIGQUERY_CREDENTIALS),
    #     project=s.GCP_PROJECT_ID,
    # )

def news_exists_today(dataset_id: str, table_id: str, news_date: date = None) -> bool:

    if news_date is None:
        news_date = date.today()
    str_date = news_date.isoformat()
    query = f"""
        SELECT COUNT(1) AS cnt
        FROM `{dataset_id}.{table_id}`
        WHERE date = '{str_date}'
        """

    client = get_bigquery_client()
    result = client.query(query).result()
    for row in result:
        return row.cnt > 0

def fetch_today_news(dataset_id: str, table_id: str, news_date: date = None) -> list[str]:
    if news_date is None:
        news_date = date.today()
    str_date = news_date.isoformat()

    query = f"""
        SELECT payload
        FROM `{dataset_id}.{table_id}`
        WHERE date = '{str_date}'
        ORDER BY createdat
        LIMIT 5
        """
    client = get_bigquery_client()
    result = client.query(query).result()
    return [row.payload for row in result]

def insert_news_to_bigquery(dataset_id: str, table_id: str, news_list: list):
    """
    news_list 示例：
    {
        "id": string,
        "source": string,
        "date": DATE,
        "payload": JSON,
        "createdat": TIMESTAMP
    }
    """

    client = get_bigquery_client()
    table_ref = f"{client.project}.{dataset_id}.{table_id}"
    print('tableref:', table_ref)
    now = datetime.datetime.utcnow().isoformat()  # datetime.datetime: module → class → method
    print(now)

    today = datetime.date.today().isoformat()  # datetime.date: module → class → method
    print(today)

    rows = []

    for n in news_list:
        print(n)

        row = {
            # 表要求的字段（统一赋值）
            "id": str(uuid.uuid4()),
            "source": "BBC",
            "date": today,
            "createdat": now,

            # GPT 返回的字段（原样保留）
            "payload": n,
        }

        rows.append(row)

    print(rows)
    errors = client.insert_rows_json(table_ref, rows)
    print(errors)
    if errors:
        raise RuntimeError(f"BigQuery insert failed: {errors}")