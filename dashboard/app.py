from pathlib import Path

import streamlit as st
import requests
from datetime import date
import time
BASE_DIR = Path(__file__).parent
# ======================
# 页面配置
# ======================
st.set_page_config(
    page_title="Daily News Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 全局CSS美化
st.markdown(
    """
    <style>
    a.anchor-link { display: none !important; }    
    /* 页面背景 */
    .stApp {
        background-color: #f6f3e8;
    }

    /* 卡片通用样式 */
    .card {
        background-color: #e6f2ff;        
        padding: 4px 12px;          /* 上下 padding 很小 */
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(59,130,246,0.12);
        margin-bottom: 12px;        /* 卡片间距压缩 */
    }

    /* 新闻标题 */
    .news-title {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin: 6px 0;            /* 上下空白相等 */
       /* margin-bottom: 8px; */
    }

    /* 新闻分隔线 */
    .divider {
        height: 1px;
        background-color: #d6cfe8;
        margin: 12px 0 16px 0;
    }

    /* 小标题 */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a; 
        margin: 6px 0;            /* 上下空白相等 */
       /* margin-bottom: 16px; */       
    }

    /* 正文文字 */
    .body-text {
        font-size: 15px;
        color: #374151;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* 修改页面顶部 st.title 的颜色 */
    h1 { 
        color: #8B4513 !important;  /* 棕色 */
        font-size: 40px;            /* 可调整大小 */
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("一页之间 | In One Page")

# ======================
# FastAPI 地址（替换成你部署的 URL）
# ======================
FASTAPI_URL = "http://127.0.0.1:8000/news"

# ======================
# 日期选择器
# ======================
# selected_date = st.date_input("选择日期", date.today())

# ======================
# 获取新闻函数
# ======================
def fetch_news_by_date(news_date):
    """
    调用 FastAPI 获取指定日期新闻：
    - 尝试 GET /news/{news_date}（如果有历史日期接口）
    - 如果没有历史接口，则调用 POST /news/update?news_date=...
    """
    try:
        # 尝试 GET /news/{news_date}（如果 FastAPI 支持）
        res = requests.get(f"{FASTAPI_URL}/{news_date}")
        if res.status_code == 200:
            return res.json()["news"]
        elif res.status_code == 404:
            return []  # 当日无新闻
        else:
            st.warning(f"查询新闻失败: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"请求新闻失败: {e}")
        return []

# ======================
# 页面启动自动获取当天新闻
# ======================
if "news_list" not in st.session_state:
    # 默认调用 update，获取当天新闻
    try:
        res_update = requests.post(f"{FASTAPI_URL}/update")
        if res_update.status_code == 200:
            st.session_state.news_list = res_update.json()["news"]
        else:
            st.warning(f"新闻更新失败: {res_update.status_code}")
            st.session_state.news_list = []
    except Exception as e:
        st.error(f"新闻更新请求失败: {e}")
        st.session_state.news_list = []

# ======================
# 选择日期后更新新闻
# ======================
# if selected_date != date.today() or "display_date" not in st.session_state:
#     st.session_state.news_list = fetch_news_by_date(selected_date)
#     st.session_state.display_date = selected_date

news_list = st.session_state.news_list

st.markdown(
    """
    <div class="card">
        <div class="section-title">国际新闻</div>    
    </div>
    """,
    unsafe_allow_html=True
)
# st.markdown('<div class="section-title">国际新闻</div>', unsafe_allow_html=True)

if news_list:
    for news in news_list[:5]:
        st.markdown(
            f"""
            <div class="news-title">{news}</div>
            <div class="divider"></div>
            """,
            unsafe_allow_html=True
        )
else:
    st.image(
        "https://via.placeholder.com/800x300.png?text=No+News+Today",
        use_column_width=True
    )
    st.info("当日无新闻记录")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="card">
        <div class="section-title">随想随说</div>    
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="body-text">
    我们虽然在英国，但平时真的很少看BBC新闻。做这个内容也正好可以了解一下天下大事！
    </div>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <div class="card">
        <div class="section-title">曼山私厨</div>    
    </div>
    """,
    unsafe_allow_html=True
)

image_list = [
    BASE_DIR / "imagelist" / "diningarea0.png",
    BASE_DIR / "imagelist" / "lambhotpot.png",
]

# for i in range(0, len(image_list), 2):
#     col1, col2 = st.columns(2)
#
#     with col1:
#         st.image(image_list[i], width="stretch")
#
#     if i + 1 < len(image_list):
#         with col2:
#             st.image(image_list[i + 1], width="stretch")
for img_path in image_list:
    if img_path.exists():
        img = st.image(img_path, width="stretch")
    else:
        st.error(f"图片未找到: {img_path}")
st.markdown(
    '<div class="body-text">我们私厨的用餐环境和招牌羊肉锅。有兴趣的朋友可以访问我们私厨网站： https://deng0529.github.io/ifood-kitchen/index-zh.html。</div>',
    unsafe_allow_html=True
)

# 手动选择
# manual_index = st.slider("选择图片", 0, len(image_list) - 1, st.session_state.img_index)
# st.image(image_list[manual_index], width=True)

st.markdown('</div>', unsafe_allow_html=True)

