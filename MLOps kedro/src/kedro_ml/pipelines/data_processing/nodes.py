"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.2
"""

import pandas as pd


def _validation(apps: pd.DataFrame) -> pd.DataFrame:
    # Check data Format
    apps['Date'] = pd.to_datetime(apps['Date'])
    # Check value ranges
    for x in apps.index:
        if apps.loc[x, "Distance (km)"] > 30:
            apps.loc[x, "Distance (km)"] = 30
        if apps.loc[x, "Average Speed (km/h)"] > 60:
            apps.loc[x, "Average Speed (km/h)"] = 60
        if apps.loc[x, "Average Heart rate (tpm)"] < 60:
            apps.loc[x, "Average Heart rate (tpm)"] = 60
    return apps

def _exploration(apps: pd.DataFrame) -> pd.DataFrame:
    apps.drop_duplicates(inplace = True)
    return apps

def _wrangling(apps: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicates
    apps.drop_duplicates(inplace = True)

    # Calculate the MEAN, and replace any empty values with it
    x = apps["Average Heart rate (tpm)"].mean()
    apps["Average Heart rate (tpm)"].fillna(x, inplace = True)

    # Clean rows that contain empty cells
    apps.dropna(inplace = True)

    # Rename 'Other' type to 'Walking'
    apps['Type'] = apps['Type'].str.replace('Other', 'Walking')

    return apps


def preprocess_activities(activities: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the data for activities.

    Args:
        activities: Raw data.
    Returns:
        Preprocessed data.
    """
    activities = _validation(activities)
    activities = _exploration(activities)
    activities = _wrangling(activities)

    return activities


def create_model_input_table(activities: pd.DataFrame ) -> pd.DataFrame:
    """Combines all data to create a model input table.

    Args:
        shuttles: Preprocessed data for shuttles.
        companies: Preprocessed data for companies.
        reviews: Raw data for reviews.
    Returns:
        model input table.

    """
   
    # Delete unnecessary columns
    cols_to_clean = ['Activity ID', 'Date', 'Type', 'Duration']
    activities.drop(cols_to_clean, axis=1, inplace=True)

    return activities