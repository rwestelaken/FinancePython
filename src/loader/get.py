
#import numpy as np
import csv
import pandas as pd
import datetime
import time

import sqlalchemy as sql
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from domain import Company, Measure, Price

class SecLoader():
	# postgres help from https://stackoverflow.com/questions/45608131/insert-from-csv-file-to-postgresql-table-with-integer-values-type

	def __init__( self ):
		self.engine = create_engine("postgresql://postgres:PostGres2020!@localhost/finance")
		Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def loadMeasure( self, filename ):
		t1 = time.time()
		measures = []
		with open( filename ) as f:
			reader = csv.reader(f)
			for row in reader:
				m = Measure()
				m.Source = "SEC"
				m.Ticker = row[1]
				m.StartDate = row[2]
				m.EndDate = row[3]
				m.EndTime = row[3]
				m.Measure = row[0]
				m.Amount = row[4]
				self.session.add(m)
		t2 = time.time()
		print( "reading time taken: " + str( t2-t1 ) + " seconds" )
		t1 = time.time()
		self.session.commit()
		t2 = time.time()
		print( "Loading time taken: " + str( t2-t1 ) + " seconds" )

	def loadPrice( self, filename ):
		#Date,Open,High,Low,Close,Adj Close,Volume
		t1 = time.time()
		ticker = filename[filename.rfind("/")+1:]
		#ticker = ticker.split(".")[0]
		ticker = ticker[:ticker.rfind(".")]
		print( ticker )
		with open( filename ) as f:
			reader = csv.reader(f)
			next(reader, None)  # skip the header
			for row in reader:
				if row[1] == "null":
					continue
				p = Price()
				p.source = "yahoo"
				p.ticker = ticker
				p.end_date = row[0]
				p.end_time = row[0]
				p.open = row[1]
				p.high = row[2]
				p.low = row[3]
				p.close = row[4]
				p.volume = row[6]
				p.adj_close = row[5]
				self.session.add(p)
		#self.session.bulk_insert_mappings(Price, prices, render_nulls=True)
		t2 = time.time()
		print( "reading time taken: " + str( t2-t1 ) + " seconds" )
		t1 = time.time()
		self.session.commit()
		t2 = time.time()
		print( "Loading time taken: " + str( t2-t1 ) + " seconds" )

	def getPrices( self, source, ticker ):
		query = self.session.query( Price ).filter( Price.ticker==ticker, Price.source==source)
		data_list = pd.read_sql( query.statement, self.engine ).set_index( 'end_date' )
		return data_list




