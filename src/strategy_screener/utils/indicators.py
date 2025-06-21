import pandas as pd
import numpy as np
import pandas_ta as ta
from rich.console import Console

console = Console()

class Indicators:
    """
    A class to calculate various technical indicators for a stock.
    """

    def __init__(self, market_data):
        """
        Initializes the Indicators instance with market data.

        :param market_data: A DataFrame containing the market data.
        """
        self.market_data = market_data

    def calculate_indicators(self):
        """
        Calculates various technical indicators for the stock data.
        :return: A DataFrame with the calculated indicators.
        """
        console.print("Calculating indicators...")
        for ticker, data in self.market_data.items():
            try:
                self._calculate_indicators_for_ticker(data)
            except Exception as e:
                console.print(f"Error processing {ticker}: {e}")
                continue
        console.print("Indicators calculation complete.")
        
    def _calculate_indicators_for_ticker(self, data):
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data.ta.bbands(length=20, append=True)
        data.ta.adx(length=14, append=True)
        data.ta.sma(length=50, append=True)
        data.ta.macd(append=True)
        data.ta.rsi(append=True)
        data['log_returns'] = np.log(data['Close'] / data['Close'].shift(1))
        data['hv_20'] = data['log_returns'].rolling(window=20).std() * np.sqrt(252)
        hv_window = 252
        data['min_hv'] = data['hv_20'].rolling(window=hv_window, min_periods=1).min()
        data['max_hv'] = data['hv_20'].rolling(window=hv_window, min_periods=1).max()
        data['hv_rank'] = 100 * (data['hv_20'] - data['min_hv']) / (data['max_hv'] - data['min_hv'])
        data['hv_rank'] = data['hv_rank'].fillna(50)
