import json
import logging
import requests
import streamlit as st
import pandas as pd
import math
import os
import subprocess

f = open(os.path.join("datasets", "params.json"))
params = json.load(f)

st.title("Prediction request")

st.header("Upload file csv")

uploaded_file = st.file_uploader("Choose a file CSV")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep = ",", header = 0,index_col = False)
    st.write(df)
    
    df['Distance (km)'] = df['Distance (km)'].astype('float64')
    df['Average Speed (km/h)'] = df['Average Speed (km/h)'].astype('float64')
    df['Calories Burned'] = df['Calories Burned'].astype('int64')
    df['Climb (m)'] = df['Climb (m)'].astype('int64')
    df['Average Heart rate (tpm)'] = df['Average Heart rate (tpm)'].astype('int64')
    row_number = df.shape[0]

    #df.to_json("p.json", orient = "records", date_format = "epoch", date_unit = "ms", default_handler = None)
    df_json = df.to_json (orient = "records", default_handler = None)

    #f = open('p.json')
    #data = json.load(f)
    # Convert JSON to String
    #y = json.dumps(data)


if st.button("Predict"):
    logging.info(f"Sending request to 127.0.0.1:3005/predict.")
    prediction = requests.post(
        "http://127.0.0.1:3005/predict",
        headers={"content-type": "application/json"},
        data=df_json,
        #data = '[{"Distance (km)": 26.91, "Example": 43, "Type": "Running", "Average Speed (km/h)": 11.08, "Activity ID": 5, "Date": 6, "Duration": 6, "Calories Burned": 1266, "Climb (m)": 98, "Average Heart rate (tpm)":121, "Distance (km)": 26.91, "Example": 43, "Type": "Running", "Average Speed (km/h)": 11.18, "Activity ID": 5, "Date": 6, "Duration": 5, "Calories Burned": 1296, "Climb (m)": 97, "Average Heart rate (tpm)":121}]'
        #data = '[{"Date": "2022-01-14", "Activity ID": "1b2f3d34-af23-4956-bd6d-8a08bd56a0d9", "Type": "Walking", "Distance (km)": 4.01, "Duration": "3:34", "Average Speed (km/h)": 10.58, "Calories Burned": 1400, "Climb (m)": 69, "Average Heart rate (tpm)": 118, "Quality": 10}, {"Date": "2022-01-14", "Activity ID": "1b2f3d34-af23-4956-bd6d-8a08bd56a0d9", "Type": "Walking", "Distance (km)": 4.01, "Duration": "3:34", "Average Speed (km/h)": 10.58, "Calories Burned": 1400, "Climb (m)": 79, "Average Heart rate (tpm)": 115, "Quality": 9}]'
    ).text

    prediction = prediction.replace("[", "")
    prediction = prediction.replace("]", "")
    li = prediction.split(", ")

    count = 0
    for row in li:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df.iloc[count])
        with col2:
            st.metric(label="Prediction", value=row)

        #li[count] = math.trunc(int(float(row)))
        li[count] = float("{:.3f}".format(float(row)))
        count += 1
        st.markdown("""---""")
   

    st.header("Create file csv with Upload file and prediction data")

    df['Quality'] = li
    df['Quality'] = df['Quality'].astype('float64')
    st.write(df)

    #df.to_csv(os.path.join("datasets", params["file_name_request_data"]), index=False)
    df.to_csv(os.path.join("datasets", "request_data.csv"), index=False)
    logging.info(f"File with request data created.")


    logging.info("Run run_example.py")
    os.system("python run_example.py")