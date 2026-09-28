import streamlit as st
import pandas as pd
import altair as alt
import base64

def get_base64_image(image_path):
    """Convert image file to base64 string for embedding in HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def run():

    st.title("Stunting Detection Dashboard")
    st.markdown("AI-powered malnutrition monitoring across Central Java cities.")

    header_image_path = "assets/children1.jpeg"  # replace with your image
    header_text_title = "Empowering Child Health Through AI"
    header_text_subtitle = "Advanced detection and monitoring for better nutrition outcomes"

    header_image_base64 = get_base64_image(header_image_path)

    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 30px;">
        <div style="position: relative; width: 100%; max-width: 1000px;">  <!-- width responsive -->
            <img src="data:image/png;base64,{header_image_base64}" 
                style="width: 100%; height: 400px; object-fit: cover; border-radius: 15px;">  <!-- fixed height -->
            <div style="
                position: absolute;
                top: 50%; 
                left: 50%; 
                transform: translate(-50%, -50%);
                width: 80%;
                text-align: center;
            ">
                <h1 style="margin:0; font-size: 32px; font-weight: bold; color: white;">{header_text_title}</h1>
                <p style="margin:0; font-size: 16px; color: white;">{header_text_subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", "3,230")
    col2.metric("Average Rate", "9.7%", "↑ 8.5%")
    col3.metric("Cities Monitored", "8")
    col4.metric("Risk Level", "Moderate")
    
    st.subheader("Cases by City")
    data = pd.DataFrame({
        "City": ["Semarang", "Solo", "Pekalongan", "Tegal", "Magelang", "Purwokerto", "Kudus", "Salatiga"],
        "Cases": [850, 420, 380, 290, 340, 450, 320, 180]
    })
    bar_chart = alt.Chart(data).mark_bar(color="black", opacity=0.8).encode(
        x=alt.X("City", sort=None),
        y="Cases"
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader("Severity Distribution")
    st.markdown("Breakdown of stunting cases by severity level")
    data_pie = pd.DataFrame({
        "Severity": ["Mild", "Moderate", "Severe"],
        "Percent": [45, 35, 20],
        "Color": ["#FFD700", "#FFA500", "#FF0000"]  
    })
    pie_chart = alt.Chart(data_pie, width=300, height=300).mark_arc().encode(
        theta=alt.Theta(field="Percent", type="quantitative"),
        color=alt.Color(field="Severity", type="nominal", scale=alt.Scale(range=data_pie["Color"].tolist())),
        tooltip=["Severity", "Percent"]
    )
    st.altair_chart(pie_chart)

    st.subheader("6-Month Trend")
    st.markdown("Stunting cases trend over the past 6 months")
    trend_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Cases": [1200, 1150, 1080, 1020, 980, 920]
    })
    line_chart = alt.Chart(trend_data).mark_line(color="black", point=alt.OverlayMarkDef(color="black")).encode(
        x="Month",
        y="Cases"
    )
    st.altair_chart(line_chart, use_container_width=True)

    st.subheader("Central Java Cities Performance")
    st.markdown("Stunting rates and progress across Central Java cities")

    performance_data = [
        {"City": "Semarang", "Rate": 11.3, "Cases": 850, "Population": 75000},
        {"City": "Solo", "Rate": 9.3, "Cases": 420, "Population": 45000},
        {"City": "Pekalongan", "Rate": 10.0, "Cases": 380, "Population": 38000},
        {"City": "Tegal", "Rate": 9.1, "Cases": 290, "Population": 32000},
        {"City": "Magelang", "Rate": 9.7, "Cases": 340, "Population": 35000},
        {"City": "Purwokerto", "Rate": 10.7, "Cases": 450, "Population": 42000},
        {"City": "Kudus", "Rate": 9.1, "Cases": 320, "Population": 35000},
        {"City": "Salatiga", "Rate": 8.2, "Cases": 180, "Population": 22000},
    ]

    for city in performance_data:
        st.markdown(f"**{city['City']}** - {city['Rate']}% - {city['Cases']} cases - {city['Population']} population")
        st.markdown(f"""
            <div style="background-color: #ddd; border-radius: 10px; width: 100%; height: 20px; margin-bottom: 10px;">
                <div style="
                    width: {city['Rate']}%;
                    background-color: #363636;
                    height: 100%;
                    border-radius: 10px;
                "></div>
            </div>
        """, unsafe_allow_html=True)
