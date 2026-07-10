import streamlit as st
import pandas as pd
from pathlib import Path
import time
from src.utils.flag_paths import FLAG_FILES
import src.utils.flag_paths as fp


from src.simulation.tournament import simulate_tournament

st.markdown("""
<div style="text-align:center;padding-top:10px;">

<h1 style="
font-size:60px;
color:white;
margin-bottom:0px;">

🏆 FIFA World Cup 2026

</h1>

<h2 style="
color:#FFD700;
margin-top:5px;">

AI Tournament Simulator

</h2>

<p style="
font-size:22px;
color:#CFCFCF;
width:75%;
margin:auto;">

Predict the entire FIFA World Cup using Machine Learning,
Elo Ratings, FIFA Rankings, Team Form and historical data.

</p>

</div>
""", unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("🌍 Teams",48)

with c2:
    st.metric("⚽ Matches",104)

with c3:
    st.metric("🤖 Model","Logistic")

with c4:
    st.metric("📈 Accuracy","54.2%")

st.markdown(
"""
<hr style="
border:2px solid #D4AF37;
margin-top:20px;
margin-bottom:20px;">
""",
unsafe_allow_html=True
)

with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )
import base64

def add_bg(image_file):
    with open(image_file, "rb") as f:
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

add_bg("assets/background.jpg")
st.title("🏆 FIFA World Cup 2026 Simulator")

st.write("")

simulate = st.button(
    "🚀 Start World Cup Simulation",
    use_container_width=True,
    type="primary",
)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <h2 style="
        text-align:center;
        color:white;
        margin-top:25px;
        margin-bottom:8px;
        font-size:42px;
    ">
        🌍 Qualified Teams
    </h2>

    <p style="
        text-align:center;
        color:#CCCCCC;
        font-size:18px;
        margin-bottom:35px;
    ">
        All 48 qualified nations competing in the FIFA World Cup 2026
    </p>
    """,
    unsafe_allow_html=True,
)
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FLAG_DIR = ROOT / "assets" / "flags" / "4x3"

def flag_path(team: str):
    """Return the full path to a team's flag SVG."""

    filename = FLAG_FILES.get(team)

    if filename is None:
        return None

    path = FLAG_DIR / filename

    if path.exists():
        return str(path)

    return None


import base64


def svg_to_base64(path):

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def display_round(round_name, matches):

    st.header(f"🏆 {round_name}")

    for match in matches:

        home_flag = ""
        away_flag = ""

        hp = flag_path(match["home_team"])
        ap = flag_path(match["away_team"])

        if hp:
            home_flag = svg_to_base64(hp)

        if ap:
            away_flag = svg_to_base64(ap)
        

        st.markdown(
            f"""
<div class="match-card">

<div class="match-row">

<div class="team">

<img src="data:image/svg+xml;base64,{home_flag}" width="48">

<div class="team-name">
{match["home_team"]}
</div>

</div>

<div class="score">

{match["home_goals"]} - {match["away_goals"]}

</div>

<div class="team" style="justify-content:flex-end;">

<div class="team-name" style="margin-right:12px;">
{match["away_team"]}
</div>

<img src="data:image/svg+xml;base64,{away_flag}">

</div>

</div>

<div class="winner">

🏆 Winner • {match["winner"]}

</div>

</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()


    

    st.success("Simulation Complete!")

import base64

def display_qualified_teams():

    from src.simulation.groups import load_groups

    groups = load_groups()

    teams = []

    for group in groups.values():
        teams.extend(group)

    teams = sorted(teams)

    cols_per_row = 8

    for i in range(0, len(teams), cols_per_row):

        cols = st.columns(cols_per_row)

        for col, team in zip(cols, teams[i:i + cols_per_row]):

            with col:

                fp = flag_path(team)

                st.markdown(
                    """
                    <div style="
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        justify-content:flex-start;
                        min-height:120px;
                    ">
                    """,
                    unsafe_allow_html=True,
                )

                if fp:
                    st.image(fp, width=52)

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        color:white;
                        font-size:15px;
                        font-weight:700;
                        margin-top:8px;
                        line-height:1.25;
                        min-height:42px;
                        display:flex;
                        align-items:flex-start;
                        justify-content:center;
                    ">
                        {team}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("</div>", unsafe_allow_html=True)

display_qualified_teams()
if simulate:



    progress_bar = st.progress(0)

    status = st.empty()

    status.markdown("### ⚽ Initializing Tournament...")
    progress_bar.progress(10)
    time.sleep(0.2)

    status.markdown("### 🌍 Loading Teams...")
    progress_bar.progress(25)
    time.sleep(0.2)

    status.markdown("### 📊 Simulating Group Stage...")
    progress_bar.progress(45)
    time.sleep(0.2)

    status.markdown("### ⚔️ Simulating Knockout Stage...")
    progress_bar.progress(70)

    results = simulate_tournament()

    status.markdown("### 🏆 Determining Champion...")
    progress_bar.progress(95)
    time.sleep(0.2)

    progress_bar.progress(100)

    status.markdown("## ✅ Simulation Complete!")
    time.sleep(0.5)

    progress_bar.empty()
    status.empty()

    st.divider()


    st.header("📊 Group Stage")

    for group_name, table in results["groups"].items():

            with st.expander(group_name):

                st.dataframe(
                    table,
                    use_container_width=True,
                    hide_index=True,
                )

    st.divider()

    display_round(
            "Round of 32",
            results["knockout"]["round_of_32"],
        )

    display_round(
            "Round of 16",
            results["knockout"]["round_of_16"],
        )

    display_round(
        "Quarter Finals",
        results["knockout"]["quarter_finals"],
    )
    display_round(
        "Semi Finals",
        results["knockout"]["semi_finals"],
    )
    display_round(
    "Final",
    results["knockout"]["final"],
)

# ---------------- Champion Card ----------------
    champion = results["knockout"]["champion"]
    runner_up = results["knockout"]["runner_up"]

    champion_flag = flag_path(champion)
    
    st.divider()
    
    st.header("🏆 FIFA World Cup 2026 Champion")
    
    if champion_flag:
        st.image(champion_flag, width=260)
    
    st.markdown(
        f"""
    <div style="text-align:center;">
    
    <h1 style="
    color:#FFD700;
    font-size:70px;
    margin-top:10px;
    margin-bottom:10px;
    font-weight:900;">
    🏆 {champion}
    </h1>
    
    <h2 style="
    color:white;
    margin-bottom:10px;">
    FIFA World Cup 2026 Champions
    </h2>
    
    <p style="
    color:#BDBDBD;
    font-size:22px;">
    Congratulations on lifting the trophy!
    </p>
    
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
    f"""
<div style="text-align:center;font-size:24px;">

🥇 <b>Champion:</b> {champion}

<br><br>

🥈 <b>Runner-up:</b> {runner_up}

</div>
""",
    unsafe_allow_html=True,
)
    
    st.balloons()