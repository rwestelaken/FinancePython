import time
from read import SecReader
from load import SecLoader
import os

def test():
	t1 = time.time()

	rootpath = "/home/westy/Data/finance"
	

	reader = SecReader()
	loader = SecLoader()

	years = { '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018' }
	years = { '2020' }
	months = { '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' }
	year = '2020'
	month = '02'
	#for year in years:
	#	for month in months:
	#		print(str(year) + str(month))

	rsspath = rootpath + f"/rss/{year}/{month}/"
	if not os.path.exists(rsspath):
		os.makedirs(rsspath)
	rsszippath = rootpath + f"/rsszip/{year}/{month}//"
	if not os.path.exists(rsszippath):
		os.makedirs(rsszippath)
	xbrlpath = rootpath + f"/xbrl/{year}/{month}//"
	if not os.path.exists(xbrlpath):
		os.makedirs(xbrlpath)
	otherpath = rootpath + f"/other/{year}/{month}//"
	if not os.path.exists(otherpath):
		os.makedirs(otherpath)
	datapath = rootpath + f"/data/{year}/{month}/"
	if not os.path.exists(datapath):
		os.makedirs(datapath)

	reader.downloadRSS( rsspath, year, month )

	##https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2018-07.xml
	


	for filename in os.listdir( rsspath ):
		print( filename )
		reader.downloadRSSZipFile( rsspath + filename, rsszippath )	

	for filename in os.listdir( rsszippath ):
		print( filename )
		reader.extractZipFile( rsszippath + filename, xbrlpath, otherpath )	

	##http://www.sec.gov/Archives/edgar/data/1602706/000114420418037722/lngb-20180331.xml
	##reader.readXBRL( '.\\xbrl\\admt-20180331.xml', 'admt' )
	
	for filename in os.listdir( xbrlpath ):
		print( filename )
		key = filename.split("-")[0]
		reader.readXBRL( xbrlpath + filename, key, datapath )
	
	for filename in os.listdir( datapath ):
		print( filename )
		loader.loadMeasure( datapath + filename )	


	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

