import yfinance as yf
from typing import Tuple, Union

def get_latest_price(symbol: str, period: str) -> Tuple[str, float]:
    """
    Get the datetime and closing price for the last day within the specified period for a given stock symbol.
    
    :param symbol: The stock ticker symbol.
    :param period: The period over which to retrieve data. The acceptable values are '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
    :return: A tuple where the first element is the datetime of the last available price and the second element is the closing price for that datetime.
    """
    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(period=period)
    if not historical_data.empty:
        last_datetime = str(historical_data.index[-1])  # Get last date (as a string for JSON serializability)
        last_price = historical_data['Close'][-1]  # Get last available closing price
        return (last_datetime, last_price)



