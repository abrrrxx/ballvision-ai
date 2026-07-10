import streamlit as st
from datetime import date

from src.preprocessing.rankings import get_ranking_map
from src.prediction.predictor import predict_match
from src.utils.flag_paths import FLAG_FILES
from pathlib import Path



ROOT = Path(__file__).resolve().parents[1]
import base64

import base64

def add_bg(image_name):

    image_path = ROOT / "assets" / image_name

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(10,15,25,0.75),
                    rgba(10,15,25,0.85)
                ),
                url("data:image/jpeg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="Match Predictor",
    page_icon="⚽",
    layout="wide",
)
add_bg("flag_background.jpg")



# -------------------- PAGE CONFIG --------------------



# -------------------- LOAD CSS --------------------

with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

# -------------------- TEAMS --------------------

teams = sorted(get_ranking_map().keys())

# -------------------- TITLE --------------------

st.title("⚽ Match Predictor")

st.write("")

# -------------------- TEAM SELECTION --------------------

left, right = st.columns(2)

with left:

    home_team = st.selectbox(
        "Home Team",
        teams,
        index=0,
    )

with right:

    away_team = st.selectbox(
        "Away Team",
        teams,
        index=1,
    )

# -------------------- VALIDATION --------------------

if home_team == away_team:

    st.warning("Please choose two different teams.")

    st.stop()

# -------------------- FLAGS --------------------
home_flag = FLAG_FILES.get(home_team)
away_flag = FLAG_FILES.get(away_team)

# -------------------- VS SECTION --------------------

left, center, right = st.columns([4, 2, 4])

with left:

    if home_flag:
        st.image(
            f"assets/flags/4x3/{home_flag}",
            width=140,
        )

    st.markdown(
        f"<h2 style='text-align:center'>{home_team}</h2>",
        unsafe_allow_html=True,
    )

with center:

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align:center;color:#D4AF37;'>VS</h1>",
        unsafe_allow_html=True,
    )

with right:

    if away_flag:
        st.image(
            f"assets/flags/4x3/{away_flag}",
            width=140,
        )

    st.markdown(
        f"<h2 style='text-align:center'>{away_team}</h2>",
        unsafe_allow_html=True,
    )

# -------------------- DATE --------------------

match_date = st.date_input(
    "Match Date",
    value=date.today(),
)

st.write("")

# -------------------- BUTTON --------------------

predict = st.button(
    "⚽ Predict Match",
    use_container_width=True,
)

# -------------------- PREDICTION --------------------

if predict:

    with st.spinner("Predicting Match..."):

        prediction = predict_match(
            home_team,
            away_team,
            str(match_date),
        )

    home_prob = prediction["home_win_probability"] * 100
    draw_prob = prediction["draw_probability"] * 100
    away_prob = prediction["away_win_probability"] * 100

    st.divider()

    st.subheader("📊 Match Prediction")

    p1, p2, p3 = st.columns(3)

    with p1:

        st.metric(
            label=f"{home_team}",
            value=f"{home_prob:.1f}%",
        )

    with p2:

        st.metric(
            label="🤝 Draw",
            value=f"{draw_prob:.1f}%",
        )

    with p3:

        st.metric(
            label=f"{away_team}",
            value=f"{away_prob:.1f}%",
        )

    # ---------------- WINNER ----------------

    if prediction["predicted_result"] == "home_win":

        winner = home_team

    elif prediction["predicted_result"] == "away_win":

        winner = away_team

    else:

        winner = "Draw"

    
    winner_flag = FLAG_FILES.get(winner)
    st.write("")

    st.success("🏆 Predicted Winner")

    with st.container(border=True):

     st.subheader("🏆 Predicted Winner")

    if winner_flag:
        st.image(
            f"assets/flags/4x3/{winner_flag}",
            width=120,
        )

    st.markdown(f"## {winner}")