import json
import logging
import requests
import streamlit as st
import pandas as pd
import math
import os
import subprocess
#import webbrowser

BENTOML_URL = "http://localhost:3005/"
EVIDENTLY_URL = "http://localhost:8085/"
PROMETHEUS_URL = "http://localhost:9090/"
ALERMANAGER_URL = "http://localhost:9093/"
GRAFANA_URL = "http://localhost:3000/"

f = open(os.path.join("datasets", "params.json"))
params = json.load(f)

st.title("Prediction request")

st.header("Welcome, the model is ready!")

flag = True

tab1, tab2 = st.tabs(["Predictions", "Monitor"])

with tab1:    
    st.subheader("Upload file csv")

    uploaded_file = st.file_uploader("Choose a file CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep = ",", header = 0,index_col = False)
        st.write(df)

        for usefull_column in params["numerical_features_names"]:
            if usefull_column not in df.columns:
                st.error('Error. %s column not present.' % usefull_column)
                flag = False
        
        if flag:
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
    #if st.button("evidently"):
        #os.system("start ./metrics_app/templates/data_drift_tests.html")    
        #webbrowser.open('file:///C:/Users/giorg/Documents/GitHub/MLOps/MLOps -observability/metrics_app/templates/data_drift_tests.html')

    if st.button("Predict"):
        if uploaded_file is None:
            st.error("Error. No file uploaded.")
        elif not flag:
            st.error("Error. File uploaded not correct.")
        else:
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

            tab3, tab4 = st.tabs(["Predictions", "Output file csv"])
        
            with tab3:
                st.subheader("All predictions")
                
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
        
            with tab4:
                st.subheader("Create file csv with Upload file and prediction data")

                df['Quality'] = li
                df['Quality'] = df['Quality'].astype('float64')
                st.write(df)

                #df.to_csv(os.path.join("datasets", params["file_name_request_data"]), index=False)
                df.to_csv(os.path.join("datasets", "request_data.csv"), index=False)
                logging.info(f"File with request data created.")            

            logging.info("Run scripts/run_example.py")
            os.system("python scripts/run_example.py")

with tab2:
    st.subheader("Can you monitor from:")

    st.write(f"Evidently - {EVIDENTLY_URL}")
    st.write(f"Prometheus - {PROMETHEUS_URL}")
    st.write(f"Alertmanager - {ALERMANAGER_URL}")
    st.write(f"Grafana - {GRAFANA_URL}")

    st.subheader("To see the Bentoml service:")
    
    st.write(f"Bentoml - {BENTOML_URL}")