from flask import Flask
from flask import abort
from flask import jsonify
from flask_cors import CORS, cross_origin
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

from domain import Company
from domain import Measure
from domain import Price

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index')
def index():
	return "Data Service"

@app.route('/data/api/v1/companies', methods=['POST','GET'])
def get_companies():
	"""
	Gets companies
	:return: ...
	"""
	session = get_session()
	list = session.query(Company).order_by(Company.ticker).all()
	result = [row2dict(report) for report in list]
	response = jsonify(result)
	response.status_code = 200 
	return response

@app.route('/data/api/v1/companies/<industry>', methods=['POST','GET'])
def get_companies_by_industry(industry=None):
	"""
	Gets companies
	:param: industry
	:return: ...
	"""
	if industry is None or len(industry) == 0:
		abort(404)
	session = get_session()
	list = session.query(Company).filter(Company.industry==industry).order_by(Company.ticker).all()
	result = [row2dict(report) for report in list]
	response = jsonify(result)
	response.status_code = 200 
	return response

@app.route('/data/api/v1/price/<ticker>', methods=['POST','GET'])
def get_prices_by_ticker(ticker=None):
	"""
	Gets prices
	:param ticker: stock ticker
	:return: ...
	"""
	if ticker is None or len(ticker) == 0:
		abort(404)
	engine = create_engine("postgresql://postgres:PostGres2020!@localhost/finance")
	Base.metadata.create_all(engine)
	session = sessionmaker(bind=engine)	
	list = session.query(Price).filter(Price.ticker == ticker).order_by(Price.end_date).all()
	result = [row2dict(report) for report in list]
	return jsonify(json_list = list), 200

def get_session():
	engine = create_engine("postgresql://postgres:PostGres2020!@localhost/finance")
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

def row2dict(row):
	return {
		c.name: str(getattr(row, c.name))
		for c in row.__table__.columns
	}

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8081, debug=True)

