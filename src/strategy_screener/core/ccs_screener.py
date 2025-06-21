from rich.console import Console

from strategy_screener.core.base_screener import BaseScreener
from strategy_screener.utils.trender import Trend, Trender

console = Console()

class CCSScreener(BaseScreener):

    def _screen(self, ticker, data):
    
        trend = Trender(data).determine_trend()
        if trend["Trend"] != Trend.DOWNTREND:
            return None
        
        latest = data.iloc[-1]
        recent_data = data.iloc[-10:-1]

        price = latest['Close']
        bb_middle_band = latest['BBM_20_2.0']
        sma_50 = latest['SMA_50']
        rsi = latest['RSI_14']

        is_near_middle_band = abs(price - bb_middle_band) <= (bb_middle_band * 0.2)
        is_near_sma_50 = abs(price - sma_50) <= (sma_50 * 0.2)
        is_in_rsi_zone = 40 < rsi < 60
        was_recently_oversold = (recent_data['RSI_14'] < 40).any()
        was_recently_overbought = (recent_data['RSI_14'] > 60).any()
        is_rally = is_in_rsi_zone and was_recently_oversold

        if (is_near_middle_band or is_near_sma_50):
            return {
                'Ticker': ticker,
                'Price': round(price, 2),
                'BB Middle': round(bb_middle_band, 2),
                'BB Upper': round(latest['BBU_20_2.0'], 2),
                'BB Lower': round(latest['BBL_20_2.0'], 2),
                'Distance from mean': round((price - bb_middle_band) / bb_middle_band * 100, 2),
                'HV20': round(latest['hv_20'] * 100, 2),
                'HV Rank': round(latest['hv_rank'], 2),
                'Rallying': is_rally,
                "Overbought": was_recently_overbought,
                "Oversold": was_recently_oversold
            }
        
        return None