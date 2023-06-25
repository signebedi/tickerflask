import yfinance as yf
from typing import Tuple, List, Union
from .exceptions import *

def get_latest_price(symbol: str, period: str = '1d', interval: str = '1d') -> Tuple[str, float]:
    """
    Get the datetime and closing price for the last data point within the specified period and interval for a given stock symbol.
    
    :param symbol: The stock ticker symbol.
    :param period: The period over which to retrieve data. The acceptable values are '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'. Defaults to '1d'.
    :param interval: The interval between data points in the retrieval. The acceptable values are '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'. Defaults to '1d'.
    :return: A tuple where the first element is the datetime of the last available price and the second element is the closing price for that datetime.
    :raises InvalidSymbolException: If the provided symbol is not valid.
    :raises InvalidPeriodException: If the provided period is not valid.
    :raises InvalidIntervalException: If the provided interval is not valid.
    :raises NoDataException: If no data is returned for the given symbol, period, and interval.
    """
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    
    if not isinstance(symbol, str) or len(symbol.strip()) == 0:
        raise InvalidSymbolException("Symbol must be a non-empty string.")
    if period not in valid_periods:
        raise InvalidPeriodException(f"Invalid period '{period}'. Period must be one of {valid_periods}.")
    if interval not in valid_intervals:
        raise InvalidIntervalException(f"Invalid interval '{interval}'. Interval must be one of {valid_intervals}.")
    if period not in ['1d', '5d', '7d'] and interval == '1m':
        raise ExceedsMaximumIntervalException("1-minute interval data can be fetched for a maximum of 7 days.")

    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(period=period, interval=interval)
    if historical_data.empty:
        raise NoDataException(f"No data returned for symbol '{symbol}' with period '{period}' and interval '{interval}'.")
    
    last_datetime = str(historical_data.index[-1])
    last_price = historical_data['Close'][-1]
    return (last_datetime, last_price)

def get_price_spread(symbol: str, period: str = '1d', interval: str = '1d') -> List[List[Union[str, float]]]:
    """
    Get the closing prices for each data point within the specified period and interval for a given stock symbol.
    
    :param symbol: The stock ticker symbol.
    :param period: The period over which to retrieve data. The acceptable values are '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'. Defaults to '1d'.
    :param interval: The interval between data points in the retrieval. The acceptable values are '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'. Defaults to '1d'.
    :return: A list of lists, where each inner list contains a date and the closing price for that date.
    :raises InvalidSymbolException: If the provided symbol is not valid.
    :raises InvalidPeriodException: If the provided period is not valid.
    :raises InvalidIntervalException: If the provided interval is not valid.
    :raises NoDataException: If no data is returned for the given symbol, period, and interval.
    """
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

    if not isinstance(symbol, str) or len(symbol.strip()) == 0:
        raise InvalidSymbolException("Symbol must be a non-empty string.")
    if period not in valid_periods:
        raise InvalidPeriodException(f"Invalid period '{period}'. Period must be one of {valid_periods}.")
    if interval not in valid_intervals:
        raise InvalidIntervalException(f"Invalid interval '{interval}'. Interval must be one of {valid_intervals}.")
    if period not in ['1d', '5d', '7d'] and interval == '1m':
        raise ExceedsMaximumIntervalException("1-minute interval data can be fetched for a maximum of 7 days.")

    ticker = yf.Ticker(symbol)
    historical_data = ticker.history(period=period, interval=interval)
    if historical_data.empty:
        raise NoDataException(f"No data returned for symbol '{symbol}' with period '{period}' and interval '{interval}'.")
    
    dates_prices = historical_data['Close'].reset_index().values.tolist()
    dates_prices = [[str(date), price] for date, price in dates_prices]
    return dates_prices