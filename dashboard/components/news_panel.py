# news_panel.py
import streamlit as st
import pandas as pd

def show_uk_news(df: pd.DataFrame):
    st.subheader("🇬🇧 今日国际TOP5新闻")
    date_options = df["date"].unique().tolist()
    selected_date = st.selectbox("选择日期", date_options)
    filtered = df[df["date"] == selected_date]
    for idx, row in filtered.iterrows():
        st.markdown(f"**{row['title_en']}**")
        st.text(f"{row['summary_zh']}")
