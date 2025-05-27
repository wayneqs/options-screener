import pandas as pd
import numpy as np
from rich.console import Console

console = Console()

def calculate_bollinger_bands(df, window=20, num_std=2):
    """Calculate Bollinger Bands."""
    sma_key = 'SMA_'+str(window)
    
    sma = df['Close'].rolling(window=window).mean()
    std = df['Close'].rolling(window=window).std()

    indicators = {
        sma_key: sma.squeeze(),  # Convert Series to DataFrame
        'STD': std.squeeze(),  # Convert Series to DataFrame
        'Upper Band': (sma + (std * num_std)).squeeze(),  # Convert Series to DataFrame
        'Lower Band': (sma - (std * num_std)).squeeze()  # Convert Series to DataFrame
    }

    return pd.DataFrame(indicators)

def calculate_exponential_moving_average(df, windows=[20,50,200]):
    """Calculate Exponential Moving Average."""
    for window in windows:
        df['EMA_'+str(window)] = df['Close'].ewm(span=window, adjust=False).mean()
    return df

def calculate_relative_strength_index(df, period=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    """Calculate Moving Average Convergence Divergence (MACD)."""
    df['EMA_short'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df

def calculate_average_true_range(df, period=14):
    """Calculate Average True Range (ATR)."""
    df['High-Low'] = df['High'] - df['Low']
    df['High-Prev Close'] = abs(df['High'] - df['Close'].shift(1))
    df['Low-Prev Close'] = abs(df['Low'] - df['Close'].shift(1))
    true_range = df[['High-Low', 'High-Prev Close', 'Low-Prev Close']].max(axis=1)
    df['ATR'] = true_range.rolling(window=period).mean()
    return df

def calculate_stochastic_oscillator(df, k_period=14, d_period=3):
    """Calculate Stochastic Oscillator."""
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=d_period).mean()
    return df

def calculate_on_balance_volume(df):
    """Calculate On-Balance Volume (OBV)."""
    df['OBV'] = 0
    df['OBV'] = df['Volume'].where(df['Close'] > df['Close'].shift(1), -df['Volume']).cumsum()
    return df

def calculate_volume_weighted_average_price(df):
    """Calculate Volume Weighted Average Price (VWAP)."""
    df['Cumulative Volume'] = df['Volume'].cumsum()
    df['Cumulative Price Volume'] = (df['Close'] * df['Volume']).cumsum()
    df['VWAP'] = df['Cumulative Price Volume'] / df['Cumulative Volume']
    return df

def calculate_hv20(df):
    """Calculate 20-day Historical Volatility."""
    log_returns = np.log(df['Close'] / df['Close'].shift(1))
    indicators = {
        'HV20': (log_returns.fillna(0).rolling(window=20, min_periods=1).std() * np.sqrt(252)).squeeze()  # Annualized,
    }

    return pd.DataFrame(indicators)