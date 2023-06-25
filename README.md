# tickerflask


### About

tickerflask is a Flask-based API that serves as a wrapper for the unofficial Yahoo Finance (yfinance) library. It provides two endpoints that retrieve the latest stock price and price spread data for any given stock symbol over a specified period and interval.

tickerflask is designed to provide a simple and efficient way of accessing financial data from the comfort of your own applications. Its simplicity and flexibility make it ideal for integrating financial data into your personal projects, financial models, web apps, and more.

### Installation

Clone the repository and install the dependencies locally using pip.

```bash
git clone https://github.com/yourgithubusername/tickerflask.git
cd tickerflask
pip install -e .
```

### Running the API locally

To run the API locally, navigate to the project's root directory and use the command:

```bash
python wsgi.py
```

This will start a local server at http://localhost:5000. To use this app in production, consider using a WSGI library like [gunicorn](https://gunicorn.org/).

### Endpoints

tickerflask provides two GET endpoints: get_latest_price and get_price_spread.

#### get_latest_price

This endpoint returns the date and closing price for the last available datapoint for the given stock symbol, period, and interval.

URL: /get_latest_price

Parameters:

    symbol: The stock ticker symbol. Defaults to 'AAPL'.
    period: The period over which to retrieve data. The acceptable values are '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'. Defaults to '1d'.
    interval: The interval between data points in the retrieval. The acceptable values are '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'. Defaults to '1d'.

Example: http://localhost:5000/get_latest_price?symbol=AAPL&period=1d&interval=1d

#### get_price_spread

This endpoint returns a list of dates and the corresponding closing prices for the given stock symbol, period, and interval.

URL: /get_price_spread

Parameters:

    symbol: The stock ticker symbol. Defaults to 'AAPL'.
    period: The period over which to retrieve data. The acceptable values are '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'. Defaults to '1d'.
    interval: The interval between data points in the retrieval. The acceptable values are '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'. Defaults to '1d'.

Example: http://localhost:5000/get_price_spread?symbol=AAPL&period=1d&interval=1d

#### Error Handling

The API will return a 400 status code and a descriptive error message if an invalid parameter value is provided or if there's an error while fetching the data.