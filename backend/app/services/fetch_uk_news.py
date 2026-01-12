import json
import feedparser
import requests
from openai import OpenAI
from backend.app.setting import get_settings
from bs4 import BeautifulSoup


# 获取配置实例（缓存）
settings = get_settings()

# 直接使用配置字段
openai_key = settings.OPENAI_API_KEY
openai_model = settings.OPENAI_MODEL
top_n = settings.UK_NEWS_TOP_N

client = OpenAI(api_key=openai_key)

from datetime import datetime
BBC_RSS = "http://feeds.bbci.co.uk/news/rss.xml"
TDS_RSS = "https://towardsdatascience.com/feed"

# -----------------------------
# 抓取新闻正文
# -----------------------------
def fetch_full_article(url: str) -> str:
    """抓取网页正文"""
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)
        return text
    except Exception as e:
        print(f"抓取文章失败: {url}, 错误: {e}")
        return ""

# -----------------------------
# 抓取 RSS 新闻链接
# -----------------------------
def fetch_latest_bbc_news():
    feed = feedparser.parse(BBC_RSS)
    news_list = []
    for entry in feed.entries[:top_n]:
        full_text = fetch_full_article(entry.link)
        news_list.append({
            "title_en": entry.title,
            "link": entry.link,
            "content_en": full_text
        })
    return news_list

def summarize_news_batch():
    """
    合并新闻一次调用 OpenAI，返回中文摘要
    """
    prompt = (f"You are a news expert and a Chinese-English translation specialist. "
              f"Summerize the following 5 English news articles and keep the words below 30. Then translate them into concise, fluent, "
              f"and fully meaningful Chinese."
              f"Output the final 5 of English news and 5 of Chinese news as a JSON object with keys 'news_en' and 'news_ch'. "
              f"Please ONLY output the JSON object, no extra text or numbering, and use standard double quotes for JSON. "
              )

    news_list = fetch_latest_bbc_news()

    for i, news in enumerate(news_list, 1):
        prompt += f"{i}. {news['content_en']}\n"
    # print(prompt)

    try:
        response = client.responses.create(
            model=openai_model,
            input=prompt,
            temperature=0.1,

        )
        print('re:', response)
        llm_text_dict = json.loads(response.output[0].content[0].text)
        print(llm_text_dict)
        # 假设 JSON 是从 "Final JSON object:" 后面开始的


        # 3. 转为两个 Python list
        news_en = llm_text_dict['news_en']
        news_ch = llm_text_dict['news_ch']

        # 4. 验证
        # print("英文新闻:", news_en[0])
        # print("中文新闻:", news_ch[0])
        clean_news = [line.split('.', 1)[1].strip() if '.' in line else line for line in news_ch]
        # 清理空字符串

        news_ch_clean = [x.strip() for x in clean_news if x.strip()]

        print('final:', news_ch_clean)
        return news_ch_clean

    except Exception as e:
        print("OpenAI API 调用错误:", e)

        return news_list



# 一次调用 OpenAI 生成中文摘要
# uk_news_ch = summarize_news_batch()

