import yfinance as yf
from typing import Tuple, Union

class InvalidPeriodException(Exception):
    """Raised when an invalid period is provided."""
    pass

class InvalidSymbolException(Exception):
    """Raised when an invalid stock symbol is provided."""
    pass

class NoDataException(Exception):
    """Raised when no data is returned for the given symbol and period."""
    pass

def get_latest_price(symbol: str, period: str) -> Tuple[str, float]:
    """
    Get the datetime and closing price for the last day within the specified period for a given stock symbol.
    
    :param symbol: The stock ticker symbol.
    :param period: The period over which to retrieve data. The acceptable values are '1m', '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
    :return: A tuple where the first element is the datetime of the last available price and the second element is the closing price for that datetime.
    """

    if not isinstance(symbol, str) or len(symbol.strip()) == 0:
        raise InvalidSymbolException("Symbol must be a non-empty string.")

    valid_periods = ['1m', '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    if period not in valid_periods:
        raise InvalidPeriodException(f"Invalid period '{period}'. Period must be one of {valid_periods}.")


    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(period=period)

    if historical_data.empty:
        raise NoDataException(f"No data returned for symbol '{symbol}' and period '{period}'.")

    last_datetime = str(historical_data.index[-1])
    last_price = historical_data['Close'][-1]
    return (last_datetime, last_price)


# @app.route('/stock/<symbol>/<period>', methods=['GET'])
# def stock_price(symbol, period):
#     last_datetime, price = get_latest_price(symbol, period)
#     return jsonify({ 'symbol': symbol, 'lastDatetime': last_datetime, 'price': price })