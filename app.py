import streamlit as st
import base64
from streamlit_option_menu import option_menu

import dashboard
import city_analysis
import monitoring
import settings
import stunting_detection


st.set_page_config(
    page_title="StuntingAI",
    layout="wide",
    page_icon="assets/icon_favicon.png"
)
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

icon_base64 = get_base64_image("assets/icon.png")

st.sidebar.markdown(
    f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px 0;
    ">
        <img src="data:image/png;base64,{icon_base64}"
             style="
                width: 70px;
                height: 70px;
                border-radius: 12px;
                object-fit: cover;
             ">
        <div style="display: flex; flex-direction: column; line-height: 1;">
            <h2 style="margin: 0; padding: 0; font-size: 20px;">StuntingAI</h2>
            <p style="margin: 0; padding: 0; font-size: 13px; color: gray;">
                Health Monitor
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.write("---")

menu_items = ["Dashboard", "Predict Stunting", "City Analysis", "Monitoring", "Settings"]

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=menu_items,
        icons=["house", "activity", "bar-chart", "people", "gear"],
        default_index=menu_items.index(st.session_state.page),
        styles={
            "container": {"background-color": "transparent"},
            "icon": {"color": "#000", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "font-family": "Inter, sans-serif",
                "color": "#333",
                "padding": "8px 12px",
                "border-radius": "6px",
                "margin": "4px 0",
                "font-weight": "normal"
            },
            "nav-link-selected": {
                "background-color": "#BBBBBB",
                "color": "white",
                "font-weight": "normal",
            },
        }
    )

if selected != st.session_state.page:
    st.session_state.page = selected
    st.rerun()
if st.session_state.page == "Dashboard":
    dashboard.run()
elif st.session_state.page == "Predict Stunting":
    stunting_detection.run()
elif st.session_state.page == "City Analysis":
    city_analysis.run()
elif st.session_state.page == "Monitoring":
    monitoring.run()
elif st.session_state.page == "Settings":
    settings.run()
