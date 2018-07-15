

import pandas as pd
import numpy as np


num_train_files = int(input("Enter the number of files for training? "))


### Data Preparation

# - Load the file and Add the headers
# - Converting the type of timestamp from object to timestamp64
# - Extracting the hour from timestamp
# - Based on statistical analysis, Dividing the per day data into 2 halves - Day (3am to 2pm) and Night(2pm to 3am)


def data_prep(filename):
    
    # Load the file
    data= pd.read_csv(filename, header=None)
    
    # Adding the header
    data.columns = ["TimeStamp", "Values"]
    
    return data

def timeperiod(data):
    # Convering object into Timestamp
    data['TimeStamp']=pd.to_datetime(data['TimeStamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Extracting the hour from timestamp
    data['Hour']=data['TimeStamp'].dt.hour
    
    ### Based on Statistical Distribution ####
    # Timestamp between 3am and 2pm is Day 
    # Timestamp between 2pm and 3am is Night
    # Day is 0 and Night is 1

    data.loc[(data['Hour'] >=14), 'Hour'] = 1
    data.loc[(data['Hour'] <3), 'Hour'] = 1
    data.loc[(data['Hour'] >1), 'Hour'] = 0
    
    return data


### Training

# - Concatenating the July 13, 14 and 16 data
# - Find the Interquartile range (IQR)
# - Define outliers based on 
#     - Values less than (25th percentile - 2.5* IQR)
#     - Values greater than (75th percentile + 2.5*IQR)
# - Choosen 2.5 times instead of standard 1.5 times to be more conservative and avoid False positives


trainingData_list =[]
for i in range(num_train_files):
    
    filename = input("Enter the name of {} training file? ".format(i+1))
    
    data= data_prep(filename)
    data = timeperiod(data)
    
    trainingData_list.append(data)


# Concatenating the data for training
#train_data= pd.concat([data_13, data_14, data_16])
train_data= pd.concat(trainingData_list)


def min_max(data, timeperiod):
    q75, q25 = np.percentile(data[data['Hour']==timeperiod].Values.dropna(), [75 ,25])
    iqr = q75 - q25

    # Used 2.5 times instead of 1.5 to be more conservative. Also, we had assumed no outliers in training data.
    min = q25 - (iqr*2.5)
    max = q75 + (iqr*2.5)
    
    return (min, max)

min_day, max_day = min_max(train_data,0)
min_night, max_night = min_max(train_data,1)


### Validating

# - Using outliers threshold for both day and night, validate the July 17 data
# - Write the anamolous points timestamp and values in a csv file

def inference(data, min_day, max_day, min_night, max_night):
    
    day=data[data['Hour']==0]
    night=data[data['Hour']==1]
    
    df1= day[day['Values']<min_day]
    df2= day[day['Values']>max_day]
    
    df3= night[night['Values']<min_night]
    df4= night[night['Values']>max_night]
    
    result = pd.concat([df1,df2,df3,df4])
    
    return result[['TimeStamp','Values']]


val_filename = input("Enter the name of validation file? ")
val_data= data_prep(val_filename)
val_data = timeperiod(val_data)


anomaly = inference(val_data,min_day, max_day, min_night, max_night)

# Write the file on disk
anomaly.to_csv("AnomalousData.csv")

print ("Successful Run")

