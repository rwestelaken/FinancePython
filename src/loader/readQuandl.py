import time
from read import SecReader
from load import SecLoader
import os

def test():
	t1 = time.time()
	rootpath = "C/Data/finance"
	reader = SecReader()
	loader = SecLoader()
	year = '2020'
	month = '02'
	datapath = rootpath + f"/data/{year}/{month}/"

	quandlpath = rootpath + f"/quandl/{year}/{month}/"
	if not os.path.exists(quandlpath):
		os.makedirs(quandlpath)
	
	loader.loadCompany( "../../data/company.csv" )

	tsx = loader.getCompanies( "TSX" )
	print(tsx)
	nyse = loader.getCompanies( "NYSE" )
	print(nyse)

	for item in tsx:
		key = item.ticker
		print( key )
		reader.downloadQuandlFinance(key, quandlpath)
	
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

