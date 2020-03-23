import time
from read import SecReader
import os

def test():
	t1 = time.time()
	rootpath = "/home/westy/Data/finance/"
	reader = SecReader()
	yahoopath = rootpath + f"yahoo/"
	if not os.path.exists(yahoopath):
		os.makedirs(yahoopath)
	banks = ["BNS.TO","BMO.TO","CM.TO","RY.TO","TD.TO","NA.TO"]
	tech = ["QQQ","MSFT","INTC","GOOG","AMZN","CSCO"]
	consumer = ["WN.TO","L.TO","MRU.TO","EMP-A.TO","SAP.TO"]
	utilities = ["FTS.TO","ATCO-X.TO","CU.TO"]
	rail = ["CNR.TO","CP.TO","CTC-A.TO"]
	index = ["SPY","QQQ","XIU.TO"]
	#for filename in os.listdir( datapath ):
	for key in index:
		#print( filename )
		#key = filename.split(".")[0]
		reader.downloadYahooFinance(key, yahoopath)
	
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

