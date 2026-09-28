import streamlit as st
import pickle
import pandas as pd
import os
from ai import train_model 
from groq import Groq

def run():
    st.title("AI Stunting Detection")
    st.markdown("Enter child measurements for AI-powered stunting analysis.")

    model_path = "model/model.pkl"
    
    if "model" not in st.session_state:
        if not os.path.exists("model"):
            os.makedirs("model")

        if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
            st.session_state.model = train_model()
        else:
            try:
                with open(model_path, "rb") as f:
                    st.session_state.model = pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                st.session_state.model = train_model()

    model = st.session_state.model

    if model is None:
        st.error("Error: Could not load dataset 'data_balita.csv' to train the model. Check if the CSV file exists.")
        return

    with st.form("input_form"):
        col1, col2 = st.columns(2)

        with col1:
            umur = st.number_input("Age (months)", min_value=0, max_value=60, value=12)
            gender = st.selectbox("Gender", ["Male", "Female"])

        with col2:
            height = st.number_input("Height (cm)", min_value=30.0, max_value=130.0, value=70.0)
            weight = st.number_input("Weight (kg)", min_value=2.0, max_value=40.0, value=9.0)

        submitted = st.form_submit_button("Analyze")

    if submitted:

        df_input = pd.DataFrame({
            "Umur (bulan)": [umur],
            "Tinggi Badan (cm)": [height]
        })
        pred_class = model.predict(df_input)[0]
        
        if pred_class == 1:
            prediction_result = "Stunted (High Risk)"
            st.error(f"**Prediction Result:** {prediction_result}")
            st.warning("This result is based on statistical data. Please consult a doctor.")
        else:
            prediction_result = "Normal Growth"
            st.success(f"**Prediction Result:** {prediction_result}")

        st.divider()

        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            st.info("Add your `GROQ_API_KEY` to `.streamlit/secrets.toml` to enable detailed AI advice.")
        else:
            client = Groq(api_key=api_key)

            prompt = f"""
            You are a pediatric nutritionist AI. 
            A child ({gender}, {umur} months old) has been screened.
            Measurements: Height {height} cm, Weight {weight} kg.
            Classification Result: {prediction_result}.

            Please provide:
            1. A brief analysis of their weight-for-height.
            2. 3 specific, localized (Indonesian context) nutritional meal recommendations.
            3. Parenting advice for this specific age group.
            Keep it concise and friendly.
            """

            with st.spinner("Generating detailed health insights via Groq..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="openai/gpt-oss-120b", 
                    )
                    response = chat_completion.choices[0].message.content
                    
                    st.subheader("AI Nutritionist Analysis")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"Connection to Groq API failed: {e}")