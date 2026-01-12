# kitchen_panel.py
import streamlit as st

def show_kitchen():
    st.subheader("🍜 私厨宣传")
    images = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg"
    ]
    captions = [
        "正宗山西刀削面",
        "手工拉面现场制作",
        "家庭私厨预约"
    ]
    st.image(images, caption=captions, width=400)
