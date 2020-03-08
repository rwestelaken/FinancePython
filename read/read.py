from xml.dom import minidom
import xml.etree.ElementTree as ET
import numpy as np
import csv
import pandas as pd
import datetime
import time
#import urllib.request
#import urllib.request
import zipfile
#import urllib2
import requests
import io
import os

class SecReader():

	def __init__(self):
		self.hello = "welcome to Sec Reader!"

	# xml help from https://www.datacamp.com/community/tutorials/python-xml-elementtree
	# zip help from https://stackoverflow.com/questions/9419162/download-returned-zip-file-from-url
	# "not in" help from https://stackoverflow.com/questions/38238861/python-check-if-any-element-in-a-list-is-a-key-in-dictionary
	# dataframe columns help from https://stackoverflow.com/questions/44513738/pandas-create-empty-dataframe-with-only-column-names
	# listdir help from https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
	# pandas csv append help from https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
	
	def downloadRSS( self ):
		years = { '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018' }
		years = { '2018' }
                years = { '2019' }
		months = { '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' }
		for year in years:
			for month in months:
				# https://www.sec.gov/Archives/edgar/monthly/xbrlrss-2005-04.xml
				path = "https://www.sec.gov/Archives/edgar/monthly/"
				filename = "xbrlrss-" + year + "-" + month + ".xml"
				response = requests.get( path + filename )
				if (not response):
					continue
				print( filename )
				output = open( './rss/' + filename, 'wb' )
                                output.write( response.content )
				output.close()
				

	def readRSS(self, filename):
		#xmldoc = minidom.parse(filename)
		xmldoce = ET.parse(filename)
		#itemlist = xmldoc.getElementsByTagName( 'item' )
		xmlroot = xmldoce.getroot()
		#print( len( itemlist ) )
		#print( len( itemliste ) )
		#print( itemlist[0].attributes['title'].value )
		#print( itemlist[0].getElementsByTagName('title').data )
		#for s in itemlist:
		for s in xmlroot.iter('item'):
			#print( s.tostring() )
			#print( s.getELementsByTagName('title')[0].firstChild.nodeValue )
			print( s.find('title').text )
			print( s.find('description').text )
			if ( s.find('guid') is None ):
				continue
			guid = s.find('guid').text
			print( "guid:" + guid )		
			#response = requests.get( guid, proxies=proxies )
			response = requests.get( guid )
			#output = open( 'tempzip','wb' )
			#output.write( response.read() )
			#output.close()
			#zfobj = zipfile.ZipFile( outputfilename )
			try:
                          zf = zipfile.ZipFile( io.BytesIO( response.content ) )
			  for name in zf.namelist():
				print( "file in zip: " + name )
				if (not "_" in name and name.endswith( ".xml" ) ):
					print( "extracting.." )
					uncompressed = zf.read( name )
                                        output = open( './xbrl/' + name, 'wb' )
					output.write( uncompressed )
					output.close()
                        except:
                          print('Error processing zip file')

	# xbrl context help from https://stackoverflow.com/questions/14513938/xbrl-us-gaap-contextref-standard

	def isNumeric( self, s ):
		try:
			float(s)
			return True
		except ValueError:
			return False

	def readXBRL( self, filename, ticker):
		ns_xbrli = "{http://www.xbrl.org/2003/instance}"
		ns_xbrldi = "{http://xbrl.org/2006/xbrldi}"
		ns_usgaap = "{http://fasb.org/us-gaap/yyyy-mm-dd}"
		search_explicit_member = ns_xbrli + "entity/" + ns_xbrli + "segment/" + ns_xbrldi + "explicitMember"
		search_period = ns_xbrli + "period"
		search_startDate = ns_xbrli + "startDate"
		search_endDate = ns_xbrli + "endDate"
		search_instant = ns_xbrli + "instant"
		taglen = len( ns_usgaap )

		#df = pd.DataFrame( columns=['ticker','startdate','enddate','value'] )
		xmldoce = ET.parse(filename)
		xmlroot = xmldoce.getroot()
		
		contextDict = dict()
		dataList = []
		t1 = time.time()
		for s in xmlroot:
			#print( "stag=" + s.tag )
			if ( s.tag.endswith( 'context' ) ):
				member = s.findall( search_explicit_member )
				if ( len(member) > 0 ):
					#print( member.tag )
					continue;
				key = s.attrib[ 'id' ]
				#print( "context=" + key )
				xmlperiod = s.find( search_period )
				xmlstartDate = xmlperiod.find( search_startDate )
				xmlendDate = xmlperiod.find( search_endDate )
				xmlinstant = xmlperiod.find( search_instant )
				startdate = ""
				enddate = ""
				if ( not xmlstartDate is None ):
					startdate = xmlstartDate.text
				if ( not xmlendDate is None ):
					enddate = xmlendDate.text
				if ( not xmlinstant is None ):
					enddate = xmlinstant.text
				contextDict[key] = {"startdate": startdate, "enddate": enddate }
		t2 = time.time()
		print( "Context time taken: " + str( t2-t1 ) + " seconds" )
		t1 = time.time()
		for s in xmlroot:
			if ( s.tag.startswith( '{http://fasb.org/us-gaap/' )  \
				#and not s.tag.endswith( 'TextBlock' ) \
				#and not s.tag.endswith( 'Policy' ) \
				#and not s.tag.endswith( 'Policies' ) \
				and not 'UseOfEstimates' in s.tag ):
				if ( not 'xsi:nil' in s.attrib ):
					value = s.text
					if ( value is None ):
						continue
					if ( value.startswith( '<' ) ):
						continue
					if ( not self.isNumeric( value ) ):
						continue
					key = s.tag[taglen:]
					#print( "key=" + key )
					#print( s.attrib )
					contextRef = s.attrib[ 'contextRef' ]
					context = contextDict.get( contextRef )
					if ( context is None ):
						continue
					startdate = context[ 'startdate' ]
					if ( startdate == "" ):
						startdate = '1900-01-01'
					enddate = context[ 'enddate' ]
					if ( enddate == "" ):
						enddate = '1900-01-01'
					#data = pd.DataFrame({"ticker": ticker, "startdate": startdate, "enddate": enddate, "value": value}, {key})
					#df = df.append( data )
					#df = df.append( pd.DataFrame({"ticker": ticker, "startdate": context[ 'startdate' ], "enddate": context[ 'enddate' ], "value": s.text}, {key}) )
					dataList.append( [key, ticker, startdate, enddate, value] )
		t2 = time.time()
		print( "Data time taken: " + str( t2-t1 ) + " seconds" )
		
		t1 = time.time()
		#csvname = ".\\data\\" + ticker+ ".csv"
		#df.to_csv( ".\\data\\" + ticker+ ".csv", sep=',', encoding='utf-8' )
		#if not os.path.isfile(csvname):
		#	df.to_csv(csvname, mode='a', sep=',')
		#else:
		#	df.to_csv(csvname, mode='a', sep=',', header=False)
	
		# csv help from https://stackoverflow.com/questions/14037540/writing-a-python-list-of-lists-to-a-csv-file

                csvname2 = './data2/' + ticker + '.csv'
       #         with open(csvname2, "w", encoding="utf-8") as f:
                with open(csvname2, "w") as f:
			if not os.path.isfile(csvname2):
				writer.writerow(['key', 'ticker', 'startdate', 'enddate', 'value'])
			writer = csv.writer(f, delimiter=",", lineterminator="\n")
			writer.writerows(dataList)

		t2 = time.time()
		print( "Saving time taken: " + str( t2-t1 ) + " seconds" )

		# postgres help from https://stackoverflow.com/questions/45608131/insert-from-csv-file-to-postgresql-table-with-integer-values-type

	# yahoo finance help from https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working

	def downloadYahooFinance( self, ticker ):
		url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=1529705406&period2=1532297406&interval=1d&events=history&crumb=IhP5WUwkm7I"
		url = "https://query1.finance.yahoo.com/v8/finance/chart/AA?symbol=AA&period1=0&period2=9999999999&interval=1mo&events=div%2Csplit"
		filename = ticker + ".json"
		pathandfilename = ".\\prices\\" + filename
		pathandfilename = './prices/' + filename
                response = requests.get( url )
		#print( response.content )
		#datetime.datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%dT%H:%M:%SZ')
		if (response):
			print( filename )
			output = open( pathandfilename, 'wb' )
			output.write( response.content )
			output.close()

	# quandl help from https://www.quora.com/Using-Python-whats-the-best-way-to-get-stock-data

	def downloadQuandlFinance( self, ticker ):
		import quandl
		apikey = "7CXBrupYp7tL53dHGUar"
		try:
			df = quandl.get("WIKI/" + ticker, start_date="2016-01-01", end_date="2018-01-01", api_key=apikey)
			csvname = './quandl/' + ticker + '.csv'
                        df.to_csv( csvname, sep=',', encoding='utf-8' )
			print( csvname )
		except:
			print( ticker + " is an invalid code" )


