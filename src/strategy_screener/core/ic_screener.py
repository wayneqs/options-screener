from rich.console import Console

from strategy_screener.core.base_screener import BaseScreener
from strategy_screener.utils.trender import Trend, Trender

console = Console()

class ICScreener(BaseScreener):

    def _screen(self, ticker, data):
    
        trend = Trender(data).determine_trend()
        if trend["Trend"] != Trend.RANGING:
            return None
        
        latest = data.iloc[-1]

        price = latest['Close']
        middle_band = latest['BBM_20_2.0']
        is_near_middle_band = abs(price - middle_band) <= (middle_band * 0.25)

        if is_near_middle_band:
            return {
                'Ticker': ticker,
                'Price': round(price, 2),
                'BB Middle': round(middle_band, 2),
                'BB Upper': round(latest['BBU_20_2.0'], 2),
                'BB Lower': round(latest['BBL_20_2.0'], 2),
                'Distance from mean': round((price - middle_band) / middle_band * 100, 2),
                'HV20': round(latest['hv_20'] * 100, 2),
                'HV Rank': round(latest['hv_rank'], 2)
            }
        
        return None