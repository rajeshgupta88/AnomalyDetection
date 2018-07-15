# AnomalyDetection Problem
Anomaly Detection assignment of an e-commerce company


## Problem Statement: 
As we deal with data in a time series, simple anomaly detection helps to find problems proactively.  In this assignment, the task is tocode and implement a simple anomaly detection algorithm in a time series data. 

## Algorithm:
- First check the distribution of values in the non-anomalous data
- Found bimodal distribution
- Divide the per day data into two halves - day(3am to 2pm) and night(2pm to 3am)
- Calulated the descriptive statistics for each halves
- Calculated the min_threshold and max_threshold based on Inter-Quartile rule of outliers
- Modified Inter-Quartile rule to avoid any False Positive
    min_threshold = Q1-2.5*IQR
    max_threshold = Q3+2.5*IQR
    
- Calculate the anomaly using min_threshold and max_threshold


## Training/Validating process

#### Requirements:
- Python 3.6
- Pandas
- Numpy
- Seaborn (optional- only for visualization purpose)
- Matplotlib (optional- only for visualization purpose)

#### Steps to train and validate?
- Keep all the csv files and python file in the same directory
- Cd to the path to the directory path from Terminal
- Run: python <python file>
  - It will ask you some parameters 
    - Number of files for training? (Ans. 3) in the given problem
    - Training File Names? (June13_data.csv, June14_data.csv, June16_data.csv) 
    - Validating file name? (June17_data.csv)
  
 - Prompt will say " Successful Run" if script runs successfully
 - "AnomalousData.csv" will be generated under the same directory
