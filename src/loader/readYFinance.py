import time
from read import SecReader
from load import SecLoader
import os

def test():
	t1 = time.time()
	rootpath = "c:\\Data\\finance\\"
	reader = SecReader()
	loader = SecLoader()
	yahoopath = rootpath + f"yahoo\\"
	if not os.path.exists(yahoopath):
		os.makedirs(yahoopath)
	
	#loader.deleteCompanies()
	#loader.loadCompany( "../../data/company.csv" )

	tsx = loader.getCompanies( "TSX" )
	print(tsx)
	nyse = loader.getCompanies( "NYSE" )
	print(nyse)
	
	for item in tsx:
		key = item.ticker
		print( key )
		reader.downloadYFinance(key, yahoopath)
	
	#loader.deletePrices()

	#for filename in os.listdir( yahoopath ):
	#	print( filename )
	#	loader.loadPrice( yahoopath + filename )

	df = loader.getPrices( 'yahoo', 'WPM.TO' )
	print(df)

	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

