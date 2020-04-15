import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Float 


Base = declarative_base()

class Company(Base): 
	__tablename__ = 'company'
	#id = Column( Integer, primary_key=True)
	ticker = Column( String(50), primary_key=True )
	name = Column( String(50) )
	sector = Column( String(50) )
	industry = Column( String(50) ) 

class Measure(Base):
	__tablename__ = 'measure'
	#id = Column( Integer, primary_key=True)
	ticker = Column( String(50), primary_key=True )
	start_date = Column( DateTime, primary_key=True )
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

