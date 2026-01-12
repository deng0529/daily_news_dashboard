import feedparser
from summarize import summarize_and_translate
from datetime import datetime

TDS_RSS = "https://towardsdatascience.com/feed"

def fetch_top3_ai_news():
    """
    返回 TDS RSS 的前 3 条 AI / ML 新闻摘要（中文）
    """
    feed = feedparser.parse(TDS_RSS)
    news_list = []

    for entry in feed.entries[:3]:
        summary_zh = summarize_and_translate(entry.summary)
        news_list.append({
            "date": datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d"),
            "source": "TDS",
            "title_en": entry.title,
            "summary_zh": summary_zh
        })

    return news_list
