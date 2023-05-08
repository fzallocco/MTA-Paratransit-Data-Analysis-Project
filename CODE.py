# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:33:30 2023

@author: filiz
"""
#Filippo Zallocco
#April 16, 2023
#MTA, Data Analytics Department
#Answering the three questions from the Data Analysis exercises provided in the pdf document

#Below are the packages I used to conduct my analysis and produce my findings
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_file(path=r"path"):
    
    #This method fetches the DATA.csv file in your current data directory and passes the file into the path variable.
    #Next, the path variable is mounted into the dataframe's method read_csv so that it becomes readable and easy to manipulate with Python.
    #In order to render the dataframe alterable, I resorted to fill missin values with zeros, rename columns according to their description in the data dictionary.
    #Furthermore, I dropped attributes that add no values to my analysis, such as ProviderId, Clientid, and TripId.
    #Columns featuring timestamp values have been converted into week days. I mean Monday, Tuesday, Wednesday, Thursday, and Friday.
    #The reason why I chose this strategy is because I wanted to group trips by provider into two categories, weekdays and weekends.
    #Subsequently, I further simplified weekdays and weekends into Yes and No under the column Weekday, and later replaced thos categorical values with 1s and 0s in the weekday column.
    #Finally, I deduced from the prompt that labels such as 'Authorized' and 'Completed' in the attribute 'Outcome' also needed to be converted into integer values.
    #Hence, values like 'Authorized' and 'Completed' have become 1s whereas any other value has been converted in 0.
    df = pd.read_csv(f"{path}")
    df['ProviderId'] = df['ProviderId'].fillna(0)
    df.rename(columns={ 'APtime': 'Departure_Pickup', 'APtime1':'Arrival_Pickup', 'ADtime':'Arrival_Destination'}, inplace=True)
    df.drop(columns=["ProviderId"], inplace=True, errors='ignore')
    df.drop(columns=["Clientid"], inplace=True, errors='ignore')
    df.drop(columns=["TripId"], inplace=True, errors='ignore')
    df['Day_of_week'] = df['Tripdate'].apply(lambda x: pd.Timestamp(x).day_name())
    df.drop(columns=["Tripdate"], inplace=True, errors='ignore')
    column_to_move = df.pop("Day_of_week")
    df.insert(3, "Day_of_week", column_to_move)
    df['Day_of_trip'] = df['Day_of_week'].apply(lambda x: 'Weekday' if x != 'Saturday' and x != 'Sunday' else 'Weekend')
    column_to_move = df.pop("Day_of_trip")
    df.insert(4, "Day_of_trip", column_to_move)
    df['Outcome_Int'] = df['Outcome'].apply(lambda x: 1 if x =='Authorized' or x == 'Completed' else 0)
    df.drop(columns=["Outcome"], inplace=True, errors='ignore')
    column_to_move = df.pop("Outcome_Int")
    df.insert(2, "Outcome_Int", column_to_move)
    column_to_move = df.pop("Outcome_Int")
    df.insert(2, "Outcome", column_to_move)
    df['Weekday'] = df['Day_of_trip'].apply(lambda x: 'Yes' if x == 'Weekday' else 'No' )
    df['Weekday'] = df['Weekday'].apply(lambda x: 1 if x == 'Yes' else 0 )
    column_to_move = df.pop("Weekday")
    df.insert(5, "Weekday", column_to_move)
    
    
    return df #This final satement returns a cleaned dataframe upon which I continued my analysis.

def visualize_head(data: pd.DataFrame = None):
    #For the sake of simplicity, I provided a method that returns the first five rows of the dataframe independent from any past alterations.
    
    print(data.head())

def visualize_tail(data: pd.DataFrame = None):
    #To assist data scientists, I included a method that displays the last five rows of the dataframe that is unaffected by any past modifications.
    print(data.tail())

def get_info(data: pd.DataFrame = None):
    #To clarify potential misunderstandings, I added a method that outputs the total attributes by index and the data type od their values.
    print(data.info())

def total_successful_trips_by_weekday_and_weekend(data: pd.DataFrame = None):
    #This method prints a more simplified dataframe that shows successful trips by weekdays, weekends, and providers, counting the total number of observations matching those criteria.
    df = data
    
    df_grouped = df.groupby(['Outcome', 'Day_of_trip'])[['ProviderType']].value_counts().reset_index(name='Counts')
    df_reframed = df_grouped.drop(df_grouped[(df_grouped.ProviderType != 'Primary') & (df_grouped.ProviderType != 'Broker') & (df_grouped.ProviderType != 'E-Hail')].index)
    df_success = df_reframed.drop(df_reframed[(df_reframed.Outcome != 1)].index)
    
    print(f"{df_success}\n")

def average_by_mode(data: pd.DataFrame = None):
    #This method shows the average trips conducted by the three main providers (Primary, Broker, and E-Hail) by weekday and weekends.
    df = data
    
    df_grouped = df.groupby(['Outcome', 'Day_of_trip'])[['ProviderType']].value_counts().reset_index(name='Counts')
    df_reframed = df_grouped.drop(df_grouped[(df_grouped.ProviderType != 'Primary') & (df_grouped.ProviderType != 'Broker') & (df_grouped.ProviderType != 'E-Hail')].index)
    df_stats= df_reframed[['Day_of_trip', 'ProviderType', 'Counts']].groupby(['Day_of_trip', 'ProviderType']).agg(['mean'])
    
    print(f"{df_stats}\n")
    
def percentage_by_mode(data: pd.DataFrame = None):
    #This method outputs a small tables that groups providers' percentage of trips over the total sum by weekday and weekend
    df = data
    
    df_grouped = df.groupby(['Outcome', 'Day_of_trip'])[['ProviderType']].value_counts().reset_index(name='Counts')
    df_reframed = df_grouped.drop(df_grouped[(df_grouped.ProviderType != 'Primary') & (df_grouped.ProviderType != 'Broker') & (df_grouped.ProviderType != 'E-Hail')].index)
    Percent = df_reframed.groupby(['Day_of_trip', 'ProviderType'])['Counts'].sum().rename("count")
    df_Percent = Percent / Percent.groupby(level=0).sum()
    
    print(f"{df_Percent}\n")    

def histograms(data: pd.DataFrame = None):
    #The above method fetches the dataframe and splits the string values inside Arrival_Destination into two columns.
    #then, it cleans the hours column by dropping all the values beginning with negative sign. Additionally, it converts the hours' string values into integers to be later be copied into an array.
    #Histrograms() later sorts the dataframe's rows in decsending order to set it up the hour values for a numpy array.
    #Unnecessary columns, such as minutes and hours, are then dropped from the data frame to save space and resources.
    #The data frame is also cleaned from potential missing values that might have been generated converting the aforementioned attributes.
    #A smaller data frame is finally created that includes hours as integers categorized by Outcome and Day_of_Week - I mean into 1s and 0s and days of the week.
    #An additional attribute is also created, Counts, which counts the number of observations per week day and outcome of the trip.
    #Finally, the values inside hour_int column are then copied into a numpy array upon which a Pyplot histogram is created that shows total successful trips by hour in a typical day
    df = data
    
    df[['hours', 'minutes']] = df['Arrival_Destination'].str.split(':', expand=True)
    df_cleaned=df.dropna()
    df_normalized=df_cleaned.drop(df_cleaned[df_cleaned.hours.str.startswith('-')].index)
    df_normalized['hour_int'] = pd.to_numeric(df_normalized['hours'])
    df_normalized= df_normalized.sort_values('hour_int')
    df_normalized.drop(columns=["minutes"], inplace=True, errors='ignore')
    df_normalized.drop(columns=["hours"], inplace=True, errors='ignore')
    df_normalized=df_normalized.dropna()
    df_simplified = df_normalized.groupby(['Outcome', 'Day_of_week'])['hour_int'].value_counts().reset_index(name='Counts')
    Hours = df_simplified['hour_int'].to_numpy()
    
    plt.hist(Hours, bins=10)
    plt.xlabel('Hours')
    plt.ylabel('Total Successful Trips')
    plt.title('Histogram of Trips by Hour of the day')
    plt.savefig('histogram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
def sorted_zipcode(data: pd.DataFrame = None):
    #Sorted_zipcode fetches a dataframe and drops all the rows the do not feature Primary as a service provider.
    #It further simplifies the dataframe, df, by not including hours outside rush hour, or outside the time fram 6 AM through 10 AM
    #Next, a smaller dataframe is generated to group zipcode of pickup locations by arrival times within rush hour.
    #In this case, we also produce a Counts column to reflect the frequency of observations of pickup zipcodes by rush hours.
    #Finally, sorted_zipcode returns the first ten zip codes with he highest number of pickups run by MTA's primary service from the entire data frame.
    #Such information will help the budget and provider teams understand the 10 most frequent pickup locations that MTA may not want to discontinue.
    df = data
    
    df_zip = df.drop(df[(df.ProviderType != 'Primary')].index)
    df_shortened = df_zip.drop(df_zip[(df_zip.Arrival_Pickup < '06:00') | (df_zip.Arrival_Pickup > '10:00')].index)
    df_pickup = df_shortened.drop(df_shortened[(df_shortened.Outcome != 1)].index)
    df_pickup.groupby('Arrival_Pickup')['PickZip'].value_counts().reset_index(name='Counts')
    zipcode_counts = df_pickup.groupby('PickZip')['Arrival_Pickup'].count()
    top_zipcodes = zipcode_counts.sort_values(ascending=False).head(10)
    print(f"{top_zipcodes}\n")
    
       