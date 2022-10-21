import json
import requests
import streamlit as st

st.title("Prediction request")

if st.button("Get the prediction"):
    prediction = requests.post(
        "http://127.0.0.1:3005/predict",
        headers={"content-type": "application/json"},
        data='[{"Distance (km)": 26.91, "Average Speed (km/h)": 11.08, "Calories Burned": 1266, "Climb (m)": 98, "Average Heart rate (tpm)":121}]',
    ).text
    st.write(f"{prediction}")