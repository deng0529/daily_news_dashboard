# ai.py
from fastapi import APIRouter
from app.services.fetch_ai_news import fetch_top3_ai_news
from app.services.storage_gcs import save_to_gcs_parquet
from datetime import datetime

router = APIRouter()

@router.post("/update")
def update_ai_news():
    data = fetch_top3_ai_news()
    today_str = datetime.now().strftime("%Y-%m-%d")
    save_to_gcs_parquet(data, f"ai_news/{today_str}.parquet")
    return {"status": "ok", "records": len(data)}
