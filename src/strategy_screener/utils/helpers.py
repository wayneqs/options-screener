"""Utility functions."""
import diskcache as dc
from datetime import datetime, timezone
import pytz
from datetime import time
import pandas_market_calendars as mcal
from functools import wraps

cache = dc.Cache("data/cache")

def validate_symbol(symbol: str) -> bool:
    """Validate if a stock symbol is properly formatted."""
    if not symbol or not isinstance(symbol, str):
        return False
    return symbol.isalpha() and len(symbol) <= 5

def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"

def is_market_hours():
    """Check if current GMT time is during US market hours (9:30 AM - 4:00 PM EST)"""
    # Get current GMT time
    gmt_now = datetime.now(timezone.utc)
    
    # Convert to Eastern Time
    eastern = pytz.timezone('US/Eastern')
    eastern_now = gmt_now.astimezone(eastern)
    
    # Check if it's a weekday (Monday=0, Sunday=6)
    if eastern_now.weekday() >= 5:  # Saturday or Sunday
        return False
    
    # Get NYSE calendar
    nyse = mcal.get_calendar('NYSE')
    
    # Check if today is a market holiday
    today = eastern_now.date()
    schedule = nyse.schedule(start_date=today, end_date=today)
    
    # If schedule is empty, it's a holiday
    if schedule.empty:
        return False
    
    # Market hours: 9:30 AM - 4:00 PM Eastern
    market_open = time(9, 30)
    market_close = time(16, 0)
    current_time = eastern_now.time()
    
    return market_open <= current_time <= market_close

def cached_outside_market_hours(key, ttl=43200):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If market is open, always fetch fresh data
            if is_market_hours():
                return func(*args, **kwargs)
            
            # Skip 'self' for instance methods
            cache_args = args[1:] if args else []
            cache_key_parts = [str(arg) for arg in cache_args]

            # Add kwargs to cache key
            if kwargs:
                kwargs_str = '-'.join(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key_parts.append(kwargs_str)

            k = f"{key}-{'-'.join(cache_key_parts)}" if cache_key_parts else key
            
            if k in cache:
                return cache[k]
            
            result = func(*args, **kwargs)
            cache.set(k, result, expire=ttl)
            return result
        return wrapper
    return decorator

def cached(key, ttl=86400):
    def decorator(func):
        def wrapper(*args, **kwargs):
            k = f"{key}-{'-'.join(map(str, args))}"
            if k in cache:
                return cache[k]
            result = func(*args, **kwargs)
            cache.set(k, result, expire=ttl)
            return result
        return wrapper
    return decorator