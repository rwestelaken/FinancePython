
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

class Measure(Base):
	__tablename__ = 'Measures'
	id = Column( Integer, primary_key=True)
	Ticker = Column( String(50) )
	StartDate = Column( DateTime )
	EndDate = Column( DateTime )
	EndTime = Column( DateTime(timezone=True) )
	Measure = Column( String(500) )
	Amount = Column( Float )
	

class SecLoader():
	# postgres help from https://stackoverflow.com/questions/45608131/insert-from-csv-file-to-postgresql-table-with-integer-values-type

	def __init__( self ):
		engine = create_engine("postgresql://postgres:PostGres2020!@localhost/finance")
		Base.metadata.create_all(engine)
		Session = sessionmaker(bind=engine)
		self.session = Session()

	def loadToPortgres( self, filename ):
		t1 = time.time()
		measures = []
		with open( filename ) as f:
			reader = csv.reader(f)
			for row in reader:
				m = Measure()
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





