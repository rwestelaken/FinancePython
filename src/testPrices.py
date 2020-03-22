import time
from read import SecReader
import os

def test():
	t1 = time.time()
	rootpath = "/home/westy/Data/finance"
	reader = SecReader()
	year = '2020'
	month = '02'
	datapath = rootpath + f"/data/{year}/{month}/"

	quandlpath = rootpath + f"/quandl/{year}/{month}/"
	if not os.path.exists(quandlpath):
		os.makedirs(quandlpath)
	
	for filename in os.listdir( datapath ):
		print( filename )
		key = filename.split(".")[0]
		reader.downloadQuandlFinance(key, quandlpath)
	
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

