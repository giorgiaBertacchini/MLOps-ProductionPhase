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

def new_tag():
    os.system('docker images --filter=reference=activities_model --format "table TAG={{.Tag}}" > tag.txt')

    fp = open("tag.txt")
    for i, line in enumerate(fp):
        if i == 1:
            ff=open(".env", "w")
            ff.write(line)
            ff.close()
            break
    fp.close()

def new_reference():
    response = requests.get(
        "http://127.0.0.1:3030/dvc_file"
    )
    myFile = open("datasets/DATA.csv.dvc", "w")
    myFile.write(response.text)
    myFile.close()

    logging.info("Pull reference dataset from Google Drive.")
    os.system("dvc pull --force")        
    logging.info("Success.")

    st.caption("Pull reference dataset from Google Drive successfully.")
    reference = pd.read_csv('datasets/DATA.csv')
    st.write(reference)

st.title("Production platform")

st.header("Welcome, the model is ready!")

flag = True

tab1, tab2, tab3, tab4 = st.tabs(["Predictions", "Monitor", "Complete Retrain", "Single actions"])


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

            tab10, tab20 = st.tabs(["Predictions", "Output file csv"])
        
            with tab10:
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
        
            with tab20:
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

    st.subheader("To see alerts received:")
    
    st.markdown(f"Slack Chat in **_monitoring_** channel")

with tab3:
    st.subheader("Is drift verified?")
    st.markdown("If yes, you should retrain the model with new dataset. Press the button.")

    st.caption("What do the next:")
    st.caption("    - Send new Dataset on train model,")
    st.caption("    - Retrain the model (push dvc dataset, mlflow run, build and dockerize bento),")
    st.caption("    - Update reference dataset in production,")
    st.caption("    - Update model in production (update tag).")

    new_dataset = st.file_uploader("Choose a file CSV as new reference dataset", type="csv")
    if new_dataset is not None:
        df_ref = pd.read_csv(new_dataset, sep = ",", header = 0,index_col = False)
        st.write(df_ref)

        df_ref_json = df_ref.to_json (orient = "records", default_handler = None)

        if st.button("Load and retrain"):
            logging.info("Load new dataset to create new model and retrain the model.")    
            prediction = requests.post(
                "http://127.0.0.1:3030/load_new_data",
                headers={"content-type": "application/json"},
                data=df_ref_json,
            ).text  

            logging.info("Update reference dataset.")
            new_reference()

            logging.info("Update tag about model.")      
            new_tag()

            logging.info("End. Complete retrain")


with tab4:
    st.subheader("Retrain model?")
    st.markdown("If you should retrain the model with the same dataset.")
    st.caption("Press the button to retrain the model.")
    if st.button("Retrain only"):
        logging.info("Retrain the model.")
        response = requests.get(
            "http://127.0.0.1:3030/retrain"
        )
        st.write("status code: ", response.status_code)        
        logging.info("End Retrain")

    st.markdown("""---""")

    st.subheader("Build Bento?")
    st.markdown("If you need new bento, yoou should build and dockerize bento")
    st.caption("Press the button to build and dockerize bento.")
    if st.button("Bento"):
        logging.info("Build and dockerize bento.")
        response = requests.get(
            "http://127.0.0.1:3030/bento"
        )
        st.write("status code: ", response.status_code)        
        logging.info("End Build Bento")
    
    st.markdown("""---""")

    st.subheader("Reference dataset changed?")
    st.markdown("If yes, you should update reference dataset of monitoring sector.")
    st.caption("Press the button to pull dvc dataset from Google Drive.")
    if st.button("Update Reference"):
        new_reference()
        logging.info("End Update Reference")

    st.markdown("""---""")

    st.subheader("Update model in monitoring sector?")
    st.markdown("If you should update the model you need new model tag.")
    st.caption("Press the button to update new model tag.")
    if st.button("Update Model"):
        logging.info("Search new model tag.")
        new_tag()
        logging.info("End Update Model.")