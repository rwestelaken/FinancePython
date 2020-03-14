import time
#from read import SecReader
from load import SecLoader
import os

def test():
	t1 = time.time()
	#reader = SecReader()
	loader = SecLoader()

	years = { '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018' }
	months = { '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' }
	#for year in years:
	#	for month in months:
	#		print(str(year) + str(month))
	#		self.downloadRSS(year, month)

	##https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2018-07.xml
	
	#for filename in os.listdir( './rss/' ):
	#	print( filename )
	#	reader.downloadRSSZipFile( './rss/' + filename )	

	#for filename in os.listdir( './rsszip/' ):
	#	print( filename )
	#	reader.extractZipFile( './rsszip/' + filename )	

	##http://www.sec.gov/Archives/edgar/data/1602706/000114420418037722/lngb-20180331.xml
	##reader.readXBRL( '.\\xbrl\\admt-20180331.xml', 'admt' )
	
	#for filename in os.listdir( './xbrl/' ):
	#	print( filename )
	#	key = filename.split("-")[0]
	#	reader.readXBRL( './xbrl/' + filename, key )
	
	for filename in os.listdir( "/home/westy/Data/finance/2019/01" ):
		print( filename )
		loader.loadToPortgres( "/home/westy/Data/finance/2019/01/" + filename )	

	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

