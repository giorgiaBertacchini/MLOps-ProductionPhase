import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

################################
########## DATA PREP ###########
################################
print('########################')
print('##### DATA PREP ########')
print('########################')

########## INGESTION ##########

# Load in the data
apps = pd.read_csv('datasets/DATA.csv')

# display stats about data
print(apps.describe())

# Print the total number of apps
print('Total number of apps in the dataset = ', apps.size)

########## VALIDATION ##########

#Check for null values
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

########## EXPLORATION ##########
#print(apps['Distance (km)'].hist())
print(apps.corr())

########## WRANGLING ##########

# Drop duplicates
apps.drop_duplicates(inplace = True)

# Print the total number of apps
print('Total number of apps in the dataset without duplicates = ', apps.size)
print(apps.columns.values)

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


########## SPLITTING ##########

# Split into train and test sections
y = apps.pop("Quality")
X_train, X_test, y_train, y_test = train_test_split(apps, y, test_size=0.33, random_state=42)

print('\nPrinting X_train...\n', X_train)
print('\nPrinting X_test...\n', X_test)
print('\nPrinting y_train...\n', y_train)
print('\nPrinting y_test...\n', y_test)

###############################
########## MODELLING ##########
###############################

########## TRAINING ##########

# Fit a model on the train section
regr = RandomForestRegressor(max_depth=2, random_state=42)
regr.fit(X_train, y_train)

# Report training set score
train_score = regr.score(X_train, y_train) * 100
# Report test set score
test_score = regr.score(X_test, y_test) * 100

# Print score
print('\nPrinting train_score...\n', train_score)
print('\nPrinting test_score...\n', test_score)


########## PREDICTING ##########

# generate predictions
ypred = regr.predict(X_test)

mse = mean_squared_error(y_test, ypred)
print("MSE: ", mse)