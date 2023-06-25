import unittest
import yfinance as yf
from unittest.mock import patch, MagicMock
from tickerflask.wrappers import get_latest_price, get_price_spread
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


if __name__ == '__main__':
    unittest.main()