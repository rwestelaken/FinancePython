
#import numpy as np
import csv
#import pandas as pd
import datetime
import time

import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class company(Base): 
	__tablename__ = 'measure'
	id = Column( Integer, primary_key=True)
	ticker = Column( String(50) )
	name = Column( String(50) )
	sector = Column( String(50) )
	industry = Column( String(50) ) 

class Measure(Base):
	__tablename__ = 'measure'
	id = Column( Integer, primary_key=True)
	ticker = Column( String(50) )
	start_date = Column( DateTime )
	end_date = Column( DateTime )
	end_time = Column( DateTime(timezone=True) )
	measure = Column( String(500) )
	amount = Column( Float )

CREATE Price(Base):
	__tablename__ = 'price'
	id = Column( Integer, primary_key=True)	source = Column( String(50) )
	source = Column( String(50) )
	ticker = Column( String(50) )
	end_date = Column( DateTime )
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
		engine = create_engine("postgresql://postgres:PostGres2020!@localhost/finance")
		Base.metadata.create_all(engine)
		Session = sessionmaker(bind=engine)
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
		prices = []
		ticker = filename[filename.rfind("/")+1:]
		ticker = ticker.split(".")[0]
		with open( filename ) as f:
			reader = csv.reader(f)
			next(reader, None)  # skip the header
			for row in reader:
				p = Price()
				p.source = "yahoo"
				p.ticker = ticker
				p.end_date = row[1]
				p.end_time = row[1]
				p.open = row[2]
				p.high = row[3]
				p.low = row[4]
				p.close = row[5]
				p.volumne = row[7]
				p.adj_close = row[6]
				self.session.add(p)
		t2 = time.time()
		print( "reading time taken: " + str( t2-t1 ) + " seconds" )
		t1 = time.time()
		self.session.commit()
		t2 = time.time()
		print( "Loading time taken: " + str( t2-t1 ) + " seconds" )




