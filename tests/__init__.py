import unittest
import yfinance as yf
import pandas as pd
from unittest.mock import patch, MagicMock
from tickerflask.wrappers import get_latest_price, get_price_spread, get_dividend_frequency, get_dividend_report
from tickerflask.exceptions import *


class TestGetLatestPrice(unittest.TestCase):
    @patch('tickerflask.wrappers.yf.Ticker')
    def test_valid_input(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = False  # Explicitly set empty to False
        mock_history.index = ['2023-07-01']  # Set some dummy data
        mock_history.__getitem__.return_value = [140.0]  # Set some dummy data
        mock_ticker.return_value.history.return_value = mock_history

        result = get_latest_price('AAPL', '1d', '1d')
        self.assertIsNotNone(result)

    def test_invalid_symbol(self):
        with self.assertRaises(InvalidSymbolException):
            get_latest_price('', '1d', '1d')

    def test_invalid_period(self):
        with self.assertRaises(InvalidPeriodException):
            get_latest_price('AAPL', 'abc', '1d')

    def test_invalid_interval(self):
        with self.assertRaises(InvalidIntervalException):
            get_latest_price('AAPL', '1d', 'abc')

    def test_exceeds_max_interval(self):
        with self.assertRaises(ExceedsMaximumIntervalException):
            get_latest_price('AAPL', '1mo', '1m')

    @patch('tickerflask.wrappers.yf.Ticker')
    def test_no_data_exception(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = True
        mock_ticker.history.return_value = mock_history

        with self.assertRaises(NoDataException):
            get_latest_price('AAPL', '1d', '1d')


class TestGetPriceSpread(unittest.TestCase):
    @patch('tickerflask.wrappers.yf.Ticker')
    def test_valid_input(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = False  # Explicitly set empty to False
        mock_history.__getitem__.return_value.reset_index.return_value.values.tolist.return_value = [['2023-07-01', 140.0]]  # Set some dummy data
        mock_ticker.return_value.history.return_value = mock_history

        result = get_price_spread('AAPL', '1d', '1d')
        self.assertIsNotNone(result)

    def test_invalid_symbol(self):
        with self.assertRaises(InvalidSymbolException):
            get_price_spread('', '1d', '1d')

    def test_invalid_period(self):
        with self.assertRaises(InvalidPeriodException):
            get_price_spread('AAPL', 'abc', '1d')

    def test_invalid_interval(self):
        with self.assertRaises(InvalidIntervalException):
            get_price_spread('AAPL', '1d', 'abc')

    def test_exceeds_max_interval(self):
        with self.assertRaises(ExceedsMaximumIntervalException):
            get_price_spread('AAPL', '1mo', '1m')

    @patch('tickerflask.wrappers.yf.Ticker')
    def test_no_data_exception(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = True
        mock_ticker.history.return_value = mock_history

        with self.assertRaises(NoDataException):
            get_price_spread('AAPL', '1d', '1d')


class TestGetDividendFrequency(unittest.TestCase):
    def test_quarterly_dividends(self):
        dividends = pd.Series(data=[0.5]*4, index=pd.date_range(start='1/1/2022', periods=4, freq='Q'))
        self.assertEqual(get_dividend_frequency(dividends), "quarterly")

    def test_semi_annually_dividends(self):
        dividends = pd.Series(data=[0.5]*2, index=pd.date_range(start='1/1/2022', periods=2, freq='6M'))
        self.assertEqual(get_dividend_frequency(dividends), "semi-annually")

    def test_annually_dividends(self):
        dividends = pd.Series(data=[0.5], index=pd.date_range(start='1/1/2022', periods=1, freq='Y'))
        self.assertEqual(get_dividend_frequency(dividends), "annually")

    def test_irregular_dividends(self):
        dividends = pd.Series(data=[0.5, None, None, None], index=pd.date_range(start='1/1/2018', end='1/1/2022', periods=4))
        self.assertEqual(get_dividend_frequency(dividends), "irregular")

class TestGetDividendReport(unittest.TestCase):
    @patch("yfinance.Ticker")
    def test_invalid_symbol(self, mock_ticker):
        with self.assertRaises(InvalidSymbolException):
            get_dividend_report('')

    @patch("yfinance.Ticker")
    def test_no_dividends(self, mock_ticker):
        mock_ticker.return_value.dividends = pd.Series()
        with self.assertRaises(NoDataException):
            get_dividend_report('AAPL')

    @patch("yfinance.Ticker")
    def test_valid_input(self, mock_ticker):
        mock_ticker.return_value.dividends = pd.Series(data=[0.5]*4, index=pd.date_range(start='1/1/2022', periods=4, freq='Q'))
        mock_ticker.return_value.info = {'currentPrice': 150, 'trailingEps': 5}

        result = get_dividend_report('AAPL')

        self.assertEqual(result['dividend_yield'], 0.5*4/150)
        self.assertEqual(result['dividend_payout_ratio'], 0.5*4/5)
        # Add more assertions for the other fields in the report

if __name__ == '__main__':
    unittest.main()