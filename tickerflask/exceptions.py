class InvalidPeriodException(Exception):
    """Raised when an invalid period is provided."""
    pass

class InvalidIntervalException(Exception):
    """Raised when an invalid interval is provided."""
    pass

class ExceedsMaximumIntervalException(Exception):
    """Raised when the requested period and interval exceed the maximum data limit."""
    pass

class InvalidSymbolException(Exception):
    """Raised when an invalid stock symbol is provided."""
    pass

class NoDataException(Exception):
    """Raised when no data is returned for the given symbol and period."""
    pass
