import streamlit as st
from PIL import Image
import base64
from pathlib import Path

st.set_page_config(
    page_title="BallVision AI",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def load_css():

    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


def get_base64(image_path):

    with open(image_path, "rb") as img:

        return base64.b64encode(
            img.read()
        ).decode()


load_css()

img = get_base64(
    "assets/images/stadium.jpg"
)

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image:
        linear-gradient(
        rgba(5,15,30,0.72),
        rgba(5,15,30,0.82)
        ),
        url("data:image/jpg;base64,{img}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
"""
<div class="glass">
<div class="hero">

<h1>⚽ BallVision AI</h1>

<h3>AI-Powered Football Intelligence</h3>

<p>
Predict Every Match • Simulate Every Tournament
</p>

</div>
</div>

""",
unsafe_allow_html=True
)

col1,col2,col3=st.columns([1.5,2,1.5])

with col2:

    if st.button(
    "⚽ Predict Match",
    use_container_width=True,
):
     st.switch_page("pages/predictor.py")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if st.button(
    "🏆 Simulate Tournament",
    use_container_width=True,
):
     st.switch_page("pages/simulator.py")

st.markdown(
"""
<div style="text-align:center;
margin-top:120px;
color:white;
opacity:.7">

BallVision AI v1.0

</div>
""",
unsafe_allow_html=True
)
st.markdown(
"""
<div style="text-align:center;
margin-top:60px;
color:#C0C0C0;
font-size:15px">

Version 1.0 • Built by Abhimanyu Sharma

</div>
""",
unsafe_allow_html=True
)