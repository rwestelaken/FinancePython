import time
from read import SecReader
import os

def test():
	t1 = time.time()
	reader = SecReader()
        #	reader.downloadRSS()
        ##https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2018-07.xml
	
        for filename in os.listdir( './rss/' ):
            print( filename )
            reader.readRSS( './rss/' + filename )
	##http://www.sec.gov/Archives/edgar/data/1602706/000114420418037722/lngb-20180331.xml
	##reader.readXBRL( '.\\xbrl\\admt-20180331.xml', 'admt' )
	
        for filename in os.listdir( './xbrl/' ):
		print( filename )
		key = filename.split("-")[0]
                reader.readXBRL( './xbrl/' + filename, key )	
	t2 = time.time()
	print( "Total time taken: " + str( t2-t1 ) + " seconds" )

if __name__ == '__main__':
	test()

