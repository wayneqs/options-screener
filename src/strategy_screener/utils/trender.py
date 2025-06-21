from enum import Enum, auto
import pandas as pd
import pandas_ta as ta

class Trend(Enum):
    UPTREND = "Uptrend"
    DOWNTREND = "Downtrend"
    RANGING = "Ranging"
    INDETERMINATE = "Indeterminate"

class Confidence(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Trender:
    """
    A class to analyse a stock to determine trend characteristics.
    """

    def __init__(self, data):
        """
        Initializes the Trender instance with stock data.

        :param data: A DataFrame containing the stock's historical data.
        """
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        self.data = data

    def __str__(self):
        return f"Trender({self.data})"

    def __repr__(self):
        return self.__str__()
    
    def determine_trend(self):
        """
        Determines the trend characteristics of the stock.

        :return: A dictionary with trend characteristics.
        """
        trend = Trend.INDETERMINATE
        confidence = Confidence.LOW

        if self.data.empty:
            return {
                "Trend": trend,
                "Confidence": confidence
            }

        latest = self.data.iloc[-1]

        adx = latest['ADX_14']
        is_ranging_adx = adx < 20

        bandwidth = latest['BBB_20_2.0']
        low_bandwidth_threshold = self.data['BBB_20_2.0'].rolling(window=50).quantile(0.25).iloc[-1]
        is_squeezing_bb = bandwidth < low_bandwidth_threshold

        price = latest['Close']
        sma_50 = latest['SMA_50']
        is_bullish_bias = price > sma_50
        is_bearish_bias = price < sma_50

        macd_line = latest['MACD_12_26_9']
        signal_line = latest['MACDs_12_26_9']
        is_bullish_macd = macd_line > signal_line
        is_bearish_macd = macd_line < signal_line

        is_confirmed_uptrend = is_bullish_bias and is_bullish_macd
        is_confirmed_downtrend = is_bearish_bias and is_bearish_macd

        # Range determination
        if is_ranging_adx and is_squeezing_bb:
            trend = Trend.RANGING
            confidence = Confidence.HIGH
        
        # Trend determination
        elif is_confirmed_uptrend:
            trend = Trend.UPTREND
            confidence = Confidence.HIGH
        elif is_confirmed_downtrend:
            trend = Trend.DOWNTREND
            confidence = Confidence.HIGH

        # Iffy conditions
        else:
            trend = Trend.INDETERMINATE
            confidence = Confidence.HIGH

        return {
            "Trend": trend,
            "Confidence": confidence
        }