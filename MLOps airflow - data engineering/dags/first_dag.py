from datetime import datetime, timedelta
import pandas as pd
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestRegressor

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

default_args={
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1)  ## TODO 5      
    }

def get_data():
    # Load in the data
    apps = pd.read_csv('./dags/data/DATA.csv')
    print("Catch data... ")

    # Print the total number of apps
    print('Total number of apps in the dataset = ', apps.size)

    print('Data Pandas: ', apps.head())

    # Save data prepared
    apps.to_csv('./dags/data/data_manage.csv', encoding='utf-8', index=False)


def data_validation():
    # Load data prepared
    apps = pd.read_csv('./dags/data/data_manage.csv')
    
    # Check for null values
    print(apps.isnull().sum())

    # Check data Format
    apps['Date'] = pd.to_datetime(apps['Date'])

    # Check column Distance (km)
    for x in apps.index:
        if apps.loc[x, "Distance (km)"] > 30:
            apps.loc[x, "Distance (km)"] = 30

    # Check column Average Speed (km/h)
    for x in apps.index:
        if apps.loc[x, "Average Speed (km/h)"] > 60:
            apps.loc[x, "Average Speed (km/h)"] = 60

    # Check column Average Heart Rate (bpm)
    for x in apps.index:
        if apps.loc[x, "Average Heart rate (tpm)"] < 60:
            apps.loc[x, "Average Heart rate (tpm)"] = 60
        
    # Save data prepared
    apps.to_csv('./dags/data/data_manage.csv', encoding='utf-8', index=False)


def data_exploration():
    # Load data prepared
    apps = pd.read_csv('./dags/data/data_manage.csv')

    print(apps.corr())

    # Save data prepared
    apps.to_csv('./dags/data/data_manage.csv', encoding='utf-8', index=False)


def data_wrangling():
    # Load data prepared
    apps = pd.read_csv('./dags/data/data_manage.csv')

    # Drop duplicates
    apps.drop_duplicates(inplace = True)

    # Calculate the MEAN, and replace any empty values with it
    x = apps["Average Heart rate (tpm)"].mean()
    apps["Average Heart rate (tpm)"].fillna(x, inplace = True)

    # Clean rows that contain empty cells
    apps.dropna(inplace = True)

    # Rename 'Other' type to 'Walking'
    apps['Type'] = apps['Type'].str.replace('Other', 'Walking')

    # Print actual DataFrame
    print(apps.to_string()) 

    # Delete unnecessary columns
    cols_to_clean = ['Activity ID', 'Date', 'Type', 'Duration']
    apps.drop(cols_to_clean, axis=1, inplace=True)

    # Save data prepared
    apps.to_csv('./dags/data/data_manage.csv', encoding='utf-8', index=False)


def data_splitting():
    # Load data prepared
    apps = pd.read_csv('./dags/data/data_manage.csv')

    # Split into train and test sections
    y = apps.pop("Quality")
    #X_train, X_test, y_train, y_test = train_test_split(apps, y, test_size=0.33, random_state=42)
    
    # The training set should be a random selection of 80% of the original data.
    # The testing set should be the remaining 20%
    X_train = apps[:80]
    y_train = y[:80]
    X_test = apps[80:]
    y_test = y[80:]

    #print('\nPrinting X_train...\n', X_train)
    #print('\nPrinting X_test...\n', X_test)
    #print('\nPrinting y_train...\n', y_train)
    #print('\nPrinting y_test...\n', y_test)

    # Save data prepared
    apps.to_csv('./dags/data/data_manage.csv', encoding='utf-8', index=False)


with DAG(
    dag_id='first_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 9, 11)
) as dag:
    task1 = PythonOperator(
        task_id='get_data',
        python_callable=get_data,
        provide_context=True
    )

    task2 = PythonOperator(
        task_id='data_validation',
        python_callable=data_validation,
        provide_context=True
    )

    task3 = PythonOperator(
        task_id='data_exploration',
        python_callable=data_exploration,
        provide_context=True
    )

    task4 = PythonOperator(
        task_id='data_wrangling',
        python_callable=data_wrangling,
        provide_context=True
    )

    task5 = PythonOperator(
        task_id='data_splitting',
        python_callable=data_splitting,
        provide_context=True
    )

    task1 >> task2 >> task3 >> task4 >> task5