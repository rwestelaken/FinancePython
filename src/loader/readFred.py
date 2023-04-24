import time
import os
import datetime 

# pip install fredapi

from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt

def test():
	t1 = time.time()
	rootpath = "/home/westy/Data/finance/"
	rootpath = "C:\\Data\\finance\\"
	oecdpath = rootpath + f"fred/"
	if not os.path.exists(oecdpath):
		os.makedirs(oecdpath)
		
	fred = Fred(api_key='d3cd5491ca0688600a3fc9450d3a8ea7')
	#df = fred.get_series('SP500', observation_start='2015-01-01', observation_end='2016-01-01')
	df = fred.get_series('T10Y2Y', observation_start='2020-01-01', observation_end='2023-01-01')
	#https://www.newyorkfed.org/research/capital_markets/ycfaq.html#/interactive
	#https://fred.stlouisfed.org/series/T10Y3M
	#https://fred.stlouisfed.org/series/T10Y2Y
	#https://fred.stlouisfed.org/series/GDP
	#https://fred.stlouisfed.org/series/MRTSSM44X72USS
	#https://fred.stlouisfed.org/series/ICSA
	
	df.describe()   
	pd.set_option('display.max_rows', None)
	pd.set_option('display.max_columns', None)
	print(df.shape)
	print(df.dtypes)
	print(df)
	df.plot()
	plt.show()
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

