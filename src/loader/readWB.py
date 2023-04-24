import time
import os
import datetime 

# https://wbdata.readthedocs.io/en/stable/

import wbdata
import pandas as pd
import re


def test():
	t1 = time.time()
	rootpath = "/home/westy/Data/finance/"
	oecdpath = rootpath + f"oecd/"
	if not os.path.exists(oecdpath):
		os.makedirs(oecdpath)
	print( wbdata.get_source() )
	print( wbdata.get_indicator(source=1) )
	print( wbdata.search_countries('united') )
	#print( wbdata.get_data("IC.BUS.EASE.XQ", country="USA") )
	data_date = datetime.datetime(2010, 1, 1), datetime.datetime(2020, 8, 31)
	print( wbdata.get_data("IC.BUS.EASE.XQ", country=["USA", "GBR"], data_date=data_date) )
	print( wbdata.search_indicators("gdp per capita") )
	print( wbdata.get_incomelevel() )
	
	countries = [i['id'] for i in wbdata.get_country(incomelevel='HIC')]                                                                                                 
	indicators = {"IC.BUS.EASE.XQ": "doing_business", "NY.GDP.PCAP.PP.KD": "gdppc"}         
	df = wbdata.get_dataframe(indicators, country=countries, convert_date=True)   
	df.describe()   
	pd.set_option('display.max_rows', None)
	pd.set_option('display.max_columns', None)
	print(df.shape)
	print(df.dtypes)
	print(df)
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

