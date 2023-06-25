from .__metadata__ import (__name__, __author__, __credits__, __version__, 
                       __license__, __maintainer__, __email__)
from flask import Flask, request, jsonify
from .wrappers import get_latest_price, get_price_spread

app = Flask(__name__)

@app.route('/get_latest_price', methods=['GET'])
def latest_price():
    symbol = request.args.get('symbol', default = '', type = str)
    period = request.args.get('period', default = '1d', type = str)
    interval = request.args.get('interval', default = '1d', type = str)
    try:
        result = get_latest_price(symbol, period, interval)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_price_spread', methods=['GET'])
def price_spread():
    symbol = request.args.get('symbol', default = '', type = str)
    period = request.args.get('period', default = '1d', type = str)
    interval = request.args.get('interval', default = '1d', type = str)
    try:
        result = get_price_spread(symbol, period, interval)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
