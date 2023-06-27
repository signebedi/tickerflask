import yfinance as yf
import pandas as pd
from typing import Tuple, List, Union, Dict, Any
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

def get_dividend_frequency(dividends: pd.Series) -> str:
    """
    Determine the frequency of dividend payouts.
    
    :param dividends: A pandas Series of dividend payouts with DateTime index.
    :return: The frequency of the dividend payouts.
    """
    dividends_per_year = dividends.groupby(dividends.index.year).count()
    avg_dividends_per_year = dividends_per_year.mean()

    if avg_dividends_per_year >= 4:
        return "quarterly"
    elif avg_dividends_per_year >= 2:
        return "semi-annually"
    elif avg_dividends_per_year >= 1:
        return "annually"
    else:
        return "irregular"

def get_dividend_report(symbol: str) -> Dict[str, Any]:
    """
    Generate a dividend report for a given stock symbol.
    
    :param symbol: The stock ticker symbol.
    :return: A dictionary with the dividend report.
    :raises InvalidSymbolException: If the provided symbol is not valid.
    """
    if not isinstance(symbol, str) or len(symbol.strip()) == 0:
        raise InvalidSymbolException("Symbol must be a non-empty string.")

    ticker = yf.Ticker(symbol)
    dividends = ticker.dividends

    if dividends.empty:
        raise NoDataException(f"No dividend data returned for symbol '{symbol}'.")

    # Convert to dictionary and format dates as strings
    dividend_history = {str(date): dividend for date, dividend in dividends.items()}

    # Calculating Dividend Yield
    current_price = ticker.info['currentPrice']

    frequency = get_dividend_frequency(dividends)
    if frequency == "quarterly":
        annual_dividend = dividends.last('1Y').sum()
    elif frequency == "semi-annually":
        annual_dividend = dividends.last('6M').sum() * 2
    elif frequency == "annually":
        annual_dividend = dividends.last('1Y').sum()
    else:
        annual_dividend = dividends.sum()  # use with caution, as it assumes irregular dividends

    dividend_yield = annual_dividend / current_price

    # Calculating Dividend Payout Ratio
    eps = ticker.info['trailingEps']  # earnings per share
    if eps == 0:
        dividend_payout_ratio = 0
    else:
        dividend_payout_ratio = annual_dividend / eps

    # Calculating Dividend Growth (over the past five years)
    five_years_dividends = dividends.last('5Y')
    if not five_years_dividends.empty:
        dividend_growth = (five_years_dividends.iloc[-1] - five_years_dividends.iloc[0]) / five_years_dividends.iloc[0]
    else:
        dividend_growth = 0

    dividend_report = {
        'dividend_history': dividend_history,
        'dividend_yield': dividend_yield,
        'dividend_payout_ratio': dividend_payout_ratio,
        'dividend_growth_5Y': dividend_growth,
        'dividend_frequency': frequency,
    }
    return dividend_report

