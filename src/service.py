from flask import flask
from flask import abort
from flask import jsonify

app = Flask(__name__)

@app.route('/')
@app.rout('/index')
def index():
	return "Data Service"

@app.route('/data/api/v1/price/<ticker>', methods=['POST','GET']
def get_price(ticker=None):
	"""
	Gets prices
	:param ticker: stock ticker
	:return: ...
	"""
	if ticker is None or len(ticker) == 0:
		abort(404)
	
	return str(0), 200


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)

