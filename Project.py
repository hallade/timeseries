#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 02:58:12 2023
@author: ALLADE Hermann
"""
''' Importing packages'''
import numpy as np
#Importing Pandas
import pandas as pd
#Importing matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#------------------------------------------------------------
''' This part of our code is for Data Analyzing and Exploring 
Create the DataFrames for each companyby removing certain columns 
such as High and Low'''

#Importing the dataset
data = pd.read_csv("C:/timeseries/stocks.csv")
#Show the head of our dataFrame
data.head()
#Viewing Datatypes of all columns
data.info()
#Checking Size of Data
data.shape
#Checking for Null Values
data.isnull().sum()
#Description of Data in the Dataframe and rounding its values up to two decimal places
data.describe().round(2)
# Show the repeated values
data.nunique()
#Checking for Duplicate Values
data.duplicated().sum()
#Converting the “Date” column dtype from object to date
data["Date"]=pd.to_datetime(data["Date"])

# Get each group and put it in a separate DataFrame
df= data.groupby('Ticker')

dataframes = {}

for groupe, data in df:
    dataframes[groupe] = data

#  Create the DataFrames for each company
#  And Dropping columns High and Low
df_AAPL = df.get_group('AAPL').drop(['High','Low'], axis = 1)
df_GOOG = df.get_group('GOOG').drop(['High','Low'], axis = 1)
df_MSFT = df.get_group('MSFT').drop(['High','Low'], axis = 1)
df_NFLX = df.get_group('NFLX').drop(['High','Low'], axis = 1)

#-----------------------------------------------------------------
'''This part permit to store DataFrames in a dictionary with keys. 
Then to browse the DataFrames dictionary, access the x and y columns
of each DataFrame with the for loop and draw a line graph 
At the end we can visualize tthe performance in the stock market of all the companies'''

dataframes = {'AAPL': df_AAPL,
              'GOOG': df_GOOG,
              'MSFT': df_MSFT,
              'NFLX': df_NFLX}

for nom, df in dataframes.items():

    x = df['Date']
    y = df['Close']
    plt.plot(x, y, label=nom)
plt.legend() # Add a caption
plt.grid(True) # Activate the grid in the background
# Display the title on the graph
plt.title("Stock Market Performance for the last 3 Months", fontsize=12) 
plt.ylabel('Close', fontsize=12) 
plt.xlabel("Date")
plt.xticks(rotation=20)
plt.show() # Show the graph

#------------------------------------------------------------------------
'''Now let’s look at the faceted area chart, which makes it easy to compare 
the performance of different companies and identify similarities or 
differences in their stock price movements '''
# List of DataFrames
dataframes = [df_AAPL, df_GOOG, df_MSFT, df_NFLX]
# Colors to use for each DataFrame
colors = ['blue', 'orange', 'green', 'red']
Title = ['AAPL', 'GOOG', 'MSFT', 'NFLX']

# Create a subgraph 
fig, axs = plt.subplots(1, len(dataframes), sharey=True)

# Plot area charts for each DataFrame
for i, (df, color, title) in enumerate(zip(dataframes, colors, Title)):
    y = df['Close']
    axs[i].fill_between(x, y, color=color, alpha=0.8)
    axs[i].set_xlabel('Date')
    axs[i].set_title(title) 
    # Tilt x axis labels
    axs[i].tick_params(axis='x', rotation=90)
    axs[i].grid(True)
# y axis label
axs[0].set_ylabel('Closing Price', fontsize = 12)
# Show charts
plt.plot(figsize = (15,7))
plt.show()

''' This part is for analysing moving averages, which provide a useful way to identify trends 
and patterns in each company’s stock price movements over a period of time'''

# Create a list of DataFrames
dataframes = {'AAPL':df_AAPL, 'GOOG': df_GOOG, 'MSFT': df_MSFT, 'NFLX': df_NFLX}

# Define moving average windows
windows = [10, 20]

# Calculate the moving average for each DataFrame with each window
for key, df in dataframes.items():
    for window in windows:
        df['MA{}'.format(window)] = df['Close'].rolling(window=window).mean()

# Show moving average columns for each DataFrame
for key , df in dataframes.items():
    print(key)
    print(df.filter(like='MA')) #Display only the MA
    print()

'''Visualizing the moving averages of all companies'''
# APPLE Moving Averages
plt.plot(figsize = (20,7))
plt.plot(df_AAPL['Date'], df_AAPL['MA10'],color='green',label='MA10')
plt.plot(df_AAPL['Date'], df_AAPL['MA20'],color='red',label='MA20')
plt.plot(df_AAPL['Date'], df_AAPL['Close'],color='blue',label='Close')

plt.title("AAPL Moving Averages")
plt.xlabel("Date")

plt.ylabel("Value")

plt.legend(title="")
plt.grid(True)
plt.show()

# GOOGLE Moving Averages
plt.plot(figsize = (20,7))
plt.plot(df_GOOG['Date'], df_GOOG['MA10'],color='green',label='MA10')
plt.plot(df_GOOG['Date'], df_GOOG['MA20'],color='red',label='MA20')
plt.plot(df_GOOG['Date'], df_GOOG['Close'],color='blue',label='Close')

plt.title("GOOG Moving Averages")
plt.xlabel("Date")

plt.ylabel("Value")

plt.legend(title="")
plt.grid(True)
plt.show()

# MICROSOFT Moving Averages
plt.plot(figsize = (20,7))
plt.plot(df_MSFT['Date'], df_MSFT['MA10'],color='green',label='MA10')
plt.plot(df_MSFT['Date'], df_MSFT['MA20'],color='red',label='MA20')
plt.plot(df_MSFT['Date'], df_MSFT['Close'],color='blue',label='Close')

plt.title("MSFT Moving Averages")
plt.xlabel("Date")

plt.ylabel("Value")

plt.legend(title="")
plt.grid(True)
plt.show()

# NETFLIX Moving Averages
plt.plot(figsize = (20,7))
plt.plot(df_NFLX['Date'], df_NFLX['MA10'],color='green',label='MA10')
plt.plot(df_NFLX['Date'], df_NFLX['MA20'],color='red',label='MA20')
plt.plot(df_NFLX['Date'], df_NFLX['Close'],color='blue',label='Close')

plt.title("NFLX Moving Averages")
plt.xlabel("Date")

plt.ylabel("Value")

plt.legend(title="")
plt.grid(True)
plt.show()

#-----------------------------------------------------------------------------
''' This part is for analyzing the volatility of all companies. 
Volatility is a measure of how much and how often the stock price or market fluctuates 
over a given period of time.'''

# Calculating volatility for each DataFrame
volatility_df_AAPL = df_AAPL['Close'].pct_change().std()
volatility_df_GOOG= df_GOOG['Close'].pct_change().std()
volatility_df_MSFT = df_MSFT['Close'].pct_change().std()
volatility_df_NFLX= df_NFLX['Close'].pct_change().std()

# Creating a list of names for DataFrames
dataframe_names = ['AAPL', 'GOOG','MSFT', 'NFLX' ]

# Creating a DataFrame containing the volatilities
volatility_data = pd.DataFrame({'DataFrame': dataframe_names, 'Volatility': 
                                [volatility_df_AAPL, volatility_df_GOOG, volatility_df_MSFT, volatility_df_NFLX]})

# Draw the volatility bar chart 
plt.figure(figsize=(10, 6))
plt.bar(volatility_data['DataFrame'], volatility_data['Volatility'])
plt.xlabel('Company')
plt.ylabel('Volatility')
plt.title('Volatility of the Four Companies')
plt.show()

# Draw the volatility line graph
plt.figure(figsize=(10, 6))
plt.plot(volatility_data['DataFrame'], volatility_data['Volatility'], marker='o', linestyle='-')
plt.xlabel('Company')
plt.ylabel('Volatility')
plt.title('Volatility of the Four Companies')
plt.grid(True)
plt.show()

#--------------------------------------------------------------------------------------
''' This part is for analyzing the correlation 
between the stock prices of Apple and Microsoft'''

# Company symbols
company_symbol1 = "AAPL"
company_symbol2 = "MSFT"

# Extracting daily returns
returns1 = df_AAPL['Adj Close'].pct_change().reset_index(0, drop=True)
returns2 = df_MSFT['Adj Close'].pct_change().reset_index(0, drop=True)
returns1
returns2

# Calculation of correlation
correlation = returns1.corr(returns2)
correlation

# Plotting the correlation curve
plt.figure(figsize=(12, 6))
plt.plot(df_AAPL.index, returns1, label=company_symbol1)
plt.plot(df_MSFT.index, returns2, label=company_symbol2)
plt.title(f'Corrélation entre {company_symbol1} et {company_symbol2}: {correlation:.2f}')
plt.xlabel('Date')
plt.ylabel('Rendement quotidien')
plt.legend()
plt.grid(True)
plt.show()


         





