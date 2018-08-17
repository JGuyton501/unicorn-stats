#regression.py
#Python V3.6.5

#This file is for displaying the neccessary graphs in a neat format to display for regression
#Should also output the needed values, already known that p < 1E-16

#Display Graph of Tx over Time, Prices over Time, Tx vs Prices scatter + Regression


# --------------AGENDA--------------
# 1 - Give Justin Overview of why/Introduction to problem statement
# 2 - Review the data sources
# 3 - Show raw data CSV and explain variable names
# 4 - Review Section 1: Data Wrangling
# 5 - Review Section 2: Statistics
# 6 - Review Section 3: Plot Data
# 7 - Explore interpretations and hypotheses



#Imports needed to make things run
import quandl, math, scipy, csv
from scipy import stats
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np



#Section 1: Data Wrangling
#Grabbing raw data from .CSV files
#Source: etherscan.io
#
#all_charts_url	 = https://etherscan.io/charts 				# all/other sources of data
#number_tx_url	 = https://etherscan.io/chart/tx 			# no. per day
#ETH_price_url	 = https://etherscan.io/chart/etherprice 	# USD
#Parsing data into usuable list formats
#Computing new data sets based on grabbed data
#
#Small function to grab and parse data from the csv files
def grabRow(filename,index):
	#Open specified file
	with open(filename, newline='') as csvfile:
		#Open the csv reader
		file = csv.reader(csvfile, delimiter=' ', quotechar='|')
		#Parse the data and grab only the column we want
		column = [row[0].split(',')[index] for row in file]
		column = [float(entry.replace("\"","")) for entry in column[1:]]
	return column

#Grab ethPrice and txCount from the .csv files
ethPrice = grabRow('export-EtherPrice.csv', 2)

txCount =grabRow('export-TxGrowth.csv', 2)


#Setup days for each entry
timeDays = [i for i in range(len(txCount))]


#Create cumulative transactions instead of transaction growth
cumTx = []
i = 0
for tx in txCount:
	if i == (0):
		cumTx.append(tx)
		i += 1
		continue
	cumTx.append(tx + cumTx[i-1])



#Section 2:
#Run Regression and form regression line
m,b,r,p,err = scipy.stats.linregress(txCount, ethPrice)
regressionLine = [(m * point) + b for point in txCount]


#Section 3:
#Plot Data

#Figure 1: Transaction per Day
plt.title("Fig. 1\nTransactions per Day")
plt.xlabel("Time (Days)")
plt.ylabel("Transactions")
plt.plot(timeDays, txCount)
plt.show()

#Figure 2: ETH Closing Price per Day
plt.title("Fig. 2\nETH Closing Price per Day")
plt.xlabel("Time (Days)")
plt.ylabel("ETH Price (USD)")
plt.plot(timeDays, ethPrice)
plt.show()


#Figure 3: Transactions vs ETH Price Regression
plt.title("Fig. 3\nTransactions vs ETH Price Regression")
plt.xlabel("Transactions")
plt.ylabel("ETH Price (USD)")
plt.scatter(txCount, ethPrice)
plt.plot(txCount, regressionLine, color="orange")
plt.show()


