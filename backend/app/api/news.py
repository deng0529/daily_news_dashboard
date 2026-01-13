from fastapi import APIRouter
from app.services.fetch_uk_news import summarize_news_batch
from app.services.storage_gcs import news_exists_today, fetch_today_news, insert_news_to_bigquery
from app.setting import get_settings
from datetime import date

router = APIRouter()

@router.post("/news/update")
def update_uk_news():
    s = get_settings()
    if news_exists_today(s.BIGQUERY_DATASET, s.UK_TABLE_ID):
        news_list = fetch_today_news(
            dataset_id=s.BIGQUERY_DATASET,
            table_id=s.UK_TABLE_ID
        )
        print("Exist news:", news_list)
        return {
            "date": date.today().isoformat(),
            "news": news_list
        }

    else:
        news_list = summarize_news_batch()
        print('Today news:', news_list)
        insert_news_to_bigquery(
            dataset_id=s.BIGQUERY_DATASET,
            table_id=s.UK_TABLE_ID,
            news_list=news_list
        )

        return {
            "date": date.today().isoformat(),
            "news": news_list
        }

@router.get("/news/{news_date}")
def get_news_by_date(news_date: date):
    s = get_settings()
    if news_exists_today(s.BIGQUERY_DATASET, s.UK_TABLE_ID, news_date):
        news_list = fetch_today_news(
            dataset_id=s.BIGQUERY_DATASET,
            table_id=s.UK_TABLE_ID,
            news_date=news_date
        )
        return {"date": news_date.isoformat(), "news": news_list}
    else:
        return {"date": news_date.isoformat(), "news": []}
