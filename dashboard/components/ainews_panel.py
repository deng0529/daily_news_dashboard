# ai_panel.py
import streamlit as st
import pandas as pd

def show_ai_news(df: pd.DataFrame):
    st.subheader("🤖 AI / ML 新闻 TOP3")
    date_options = df["date"].unique().tolist()
    selected_date = st.selectbox("选择日期 (AI)", date_options, key="ai_date")
    filtered = df[df["date"] == selected_date]
    for idx, row in filtered.iterrows():
        st.markdown(f"**{row['title_en']}**")
        st.text(f"{row['summary_zh']}")
