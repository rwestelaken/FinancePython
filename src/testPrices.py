import time
from read import SecReader
import os

def test():
	t1 = time.time()
	reader = SecReader()
	#reader.downloadYahooFinance("aa")
	for filename in os.listdir( ".\\data2\\" ):
		print( filename )
		key = filename.split(".")[0]
		reader.downloadQuandlFinance(key)
	
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

