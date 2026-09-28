import streamlit as st
import altair as alt
import pandas as pd

def run():

    st.title("Central Java City Analytics")
    st.text("Detailed stunting analysis for Central Java cities")

    city_data = {
        "Semarang": {
            "population": "1,653,000",
            "cases": "12,450",
            "rate": "14.8%",
            "improvement": "5.1%",
            "trend": [1450, 1500, 1480, 1520, 1550, 1490],
            "districts": {
                "Semarang Tengah": 165,
                "Semarang Barat": 178,
                "Semarang Timur": 152,
                "Semarang Selatan": 195,
                "Semarang Utara": 160
            }
        },
        "Solo": {
            "population": "519,000",
            "cases": "4,320",
            "rate": "12.4%",
            "improvement": "7.3%",
            "trend": [480, 500, 470, 520, 510, 495],
            "districts": {
                "Laweyan": 82,
                "Serengan": 75,
                "Pasar Kliwon": 88,
                "Jebres": 95,
                "Banjarsari": 80
            }
        },
        "Pekalongan": {
            "population": "307,000",
            "cases": "2,150",
            "rate": "10.2%",
            "improvement": "9.4%",
            "trend": [210, 220, 205, 230, 215, 225],
            "districts": {
                "Pekalongan Barat": 85,
                "Pekalongan Timur": 78,
                "Pekalongan Utara": 92,
                "Pekalongan Selatan": 125
            }
        }
    }

    age_group_data = {
        "Semarang": [
            {"range": "0-6 months", "cases": 58, "percent": 6.8},
            {"range": "6-12 months", "cases": 167, "percent": 19.6},
            {"range": "12-24 months", "cases": 289, "percent": 34.0},
            {"range": "24-36 months", "cases": 218, "percent": 25.5},
            {"range": "36-60 months", "cases": 118, "percent": 13.9},
        ],
        "Solo": [
            {"range": "0-6 months", "cases": 29, "percent": 6.9},
            {"range": "6-12 months", "cases": 79, "percent": 18.8},
            {"range": "12-24 months", "cases": 143, "percent": 34.0},
            {"range": "24-36 months", "cases": 109, "percent": 26.0},
            {"range": "36-60 months", "cases": 60, "percent": 14.3},
        ],
        "Pekalongan": [
            {"range": "0-6 months", "cases": 26, "percent": 6.8},
            {"range": "6-12 months", "cases": 74, "percent": 19.5},
            {"range": "12-24 months", "cases": 129, "percent": 34.0},
            {"range": "24-36 months", "cases": 97, "percent": 25.5},
            {"range": "36-60 months", "cases": 54, "percent": 14.2},
        ]
    }

    city = st.selectbox("Select City", list(city_data.keys()))
    data = city_data[city]

    st.subheader(f"{city} Health Monitoring")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Population", data["population"])
    col2.metric("Stunting Cases", data["cases"])
    col3.metric("Stunting Rate", data["rate"])
    col4.metric("Improvement", data["improvement"])

    st.subheader("Monthly Trend")
    df_trend = pd.DataFrame({
        "Month": [f"M{i+1}" for i in range(len(data["trend"]))],
        "Cases": data["trend"]
    })
    line_chart = alt.Chart(df_trend).mark_line(color="black", point=alt.OverlayMarkDef(color="black")).encode(
        x="Month",
        y="Cases"
    )
    st.altair_chart(line_chart, use_container_width=True)

    st.subheader("District Analysis")
    st.markdown("Stunting cases by district/sub-area")
    df_district = pd.DataFrame({
        "District": list(data["districts"].keys()),
        "Cases": list(data["districts"].values())
    })
    bar_chart = alt.Chart(df_district).mark_bar(color="black", opacity=0.7).encode(
        x="District",
        y="Cases"
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader("Age Group Distribution")
    st.markdown("Stunting cases by age groups")

    selected_age_groups = age_group_data[city]

    for group in selected_age_groups:
        width = group["percent"]
        st.markdown(f"**{group['range']}** - {group['cases']} cases ({group['percent']}%)")
        st.markdown(f"""
            <div style="
                background-color: #ddd;
                border-radius: 10px;
                width: 100%;
                height: 20px;
                margin-bottom: 10px;
                overflow: hidden;
            ">
                <div style="
                    width: {width}%;
                    background-color: black;
                    height: 100%;
                "></div>
            </div>
        """, unsafe_allow_html=True)
