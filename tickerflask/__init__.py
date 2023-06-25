from .__metadata__ import (__name__, __author__, __credits__, __version__, 
                       __license__, __maintainer__, __email__)
from flask import Flask, request, jsonify, render_template
from .wrappers import get_latest_price, get_price_spread
import os, uuid, json, plotly
import plotly.graph_objects as go

def set_secret_key():
    # Check if the secret key file exists
    if os.path.exists('.secret_key'):
        # If it exists, read the key from the file
        with open('.secret_key', 'r') as f:
            secret_key = f.read()
    else:
        # If it doesn't exist, generate a new UUID and save it in the file
        secret_key = str(uuid.uuid4())
        with open('.secret_key', 'w') as f:
            f.write(secret_key)
    return secret_key

app = Flask(__name__)
app.secret_key = set_secret_key()
app.static_folder = 'static/'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html.jinja')

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

@app.route('/get_price_spread_plotly', methods=['GET'])
def price_spread_with_plotly():

    symbol = request.args.get('symbol', default = '', type = str)
    period = request.args.get('period', default = '1d', type = str)
    interval = request.args.get('interval', default = '1d', type = str)

    try:
        data = get_price_spread(symbol, period, interval)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


    # separate dates and prices
    dates = [dp[0] for dp in data]
    prices = [dp[1] for dp in data]

    # create line graph
    fig = go.Figure(data=go.Scatter(x=dates, y=prices))

    # add title and labels
    fig.update_layout(
        title=f"Price Spread for {symbol} over {period} with {interval} interval",
        xaxis_title="Date",
        yaxis_title="Price",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    fig.update_layout(
        plot_bgcolor='rgb(20, 20, 20)',
        paper_bgcolor='rgb(20, 20, 20)',
        font=dict(color='rgb(255, 255, 255)'),
    )

    result = {'data': data}
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    result['graphJSON'] = graphJSON

    return jsonify(result), 200