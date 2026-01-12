# thoughts_panel.py
import streamlit as st

def show_thoughts():
    st.subheader("🧠 我的想法")
    text = st.text_area("写下你的想法", value="无", height=80)
    st.text(f"当前想法：{text}")
