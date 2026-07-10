from pathlib import Path
import streamlit as st

FLAG_DIR = Path("assets/flags")


def get_flag_path(team_name: str):
    file = FLAG_DIR / f"{team_name}.svg"

    if file.exists():
        return str(file)

    return None


def show_team(team_name: str, width=40):

    flag = get_flag_path(team_name)

    col1, col2 = st.columns([1, 6])

    with col1:
        if flag:
            st.image(flag, width=width)

    with col2:
        st.markdown(
            f"<h4 style='margin-top:8px'>{team_name}</h4>",
            unsafe_allow_html=True,
        )