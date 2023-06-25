import yfinance as yf

def get_latest_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    if not todays_data.empty:
        return todays_data['Close'][0]

