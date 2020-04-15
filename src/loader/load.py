
#import numpy as np
import csv
import pandas as pd
import datetime
import time

import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class Company(Base): 
	__tablename__ = 'company'
	#id = Column( Integer, primary_key=True)
	ticker = Column( String(50), primary_key=True )
	name = Column( String(50) )
	sector = Column( String(50) )
	industry = Column( String(50) ) 
	city = Column( String(50) )
	country = Column( String(50) )
	exchange = Column( String(50) )

class Measure(Base):
	__tablename__ = 'measure'
	#id = Column( Integer, primary_key=True)
	ticker = Column( String(50), primary_key=True )
	start_date = Column( DateTime )
	end_date = Column( DateTime, primary_key=True )
	end_time = Column( DateTime(timezone=True) )
	measure = Column( String(500), primary_key=True )
	amount = Column( Float )

class Price(Base):
	__tablename__ = 'price'
	#id = Column( Integer, primary_key=True)
	source = Column( String(50), primary_key=True )
	ticker = Column( String(50), primary_key=True )
	end_date = Column( DateTime, primary_key=True )
	end_time = Column( DateTime(timezone=True) )
	open = Column( Float )
	high = Column( Float )
	low = Column( Float )
	close = Column( Float )
	volume = Column( Float )
	adj_close = Column( Float )

class SecLoader():
	# postgres help from https://stackoverflow.com/questions/45608131/insert-from-csv-file-to-postgresql-table-with-integer-values-type

	def __init__( self ):
		self.engine = create_engine("postgresql://postgres:PostGres2020!@localhost/finance")
		Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def deleteCompanies( self ):
		count = self.session.query(Company).delete()
		self.session.commit()
		print( f"{count} companies deleted" )

	def loadCompany( self, filename ):
		t1 = time.time()
		with open( filename ) as f:
			reader = csv.reader(f)
			for row in reader:
				c = Company()
				c.Source = "SEC"
				c.ticker = row[0]
				c.name = row[1]
				c.sector = row[2]
				c.industry = row[3]
				c.city = row[4]
				c.country = row[5]
				c.exchange = row[6]
				#print( c )
				self.session.add(c)
		t2 = time.time()
		print( "reading time taken: " + str( t2-t1 ) + " seconds" )
		t1 = time.time()
		self.session.commit()
		t2 = time.time()
		print( "Loading time taken: " + str( t2-t1 ) + " seconds" )

	def loadMeasure( self, filename ):
		t1 = time.time()
		measures = []
		with open( filename ) as f:
			reader = csv.reader(f)
			for row in reader:
				m = Measure()
				m.Source = "SEC"
				m.ticker = row[1]
				m.start_date = row[2]
				m.end_date = row[3]
				m.end_time = row[3]
				m.measure = row[0]
				m.amount = row[4]
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


	def getCompanies( self, exchange ):
		#query = self.session.query( Company ).filter( Company.exchange==exchange )
		#data_list = pd.read_sql( query.statement, self.engine ).set_index( 'ticker' )
		return self.session.query( Company ).filter( Company.exchange==exchange ).all()	


