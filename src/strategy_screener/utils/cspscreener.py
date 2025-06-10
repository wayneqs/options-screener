from .indicators import calculate_bollinger_bands, calculate_relative_strength_index, calculate_hv20
from rich.console import Console
import pandas as pd
import numpy as np

console = Console()

def screen(names):
    """Screen names based on various criteria."""
    results = []
    for ticker, df in names.items():
        try:
            data = screen_name(ticker, df)
            if data:
                results.append(data)
        except Exception as e:
            console.print(f"Error processing {ticker}: {e}")
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(
        by=["HV20% (Annualized)", "Distance from key level%", ],
        key=lambda col: np.abs(col) if col.name == "Distance from key level%" else col,
        ascending=[False, True]
    ).reset_index(drop=True)
    return results_df


def screen_name(ticker, ticker_df):
    """Screen stock based on various criteria."""
    bol_df = calculate_bollinger_bands(ticker_df)
    hv20_df = calculate_hv20(ticker_df)
    rsi_df = calculate_relative_strength_index(ticker_df)
    
    ticker_last = ticker_df.iloc[-1]
    bol_last = bol_df.iloc[-1]
    hv20_last = hv20_df.iloc[-1]
    rsi_last = rsi_df.iloc[-1]

    ticker_last_close = ticker_last['Close'].item()
    sma = bol_last['SMA_20'].item()
    bol_lower_band = bol_last['Lower Band'].item()
    hv20 = hv20_last['HV20'].item()
    rsi = rsi_last['RSI'].item()

    # screen out names that have a high RSI
    if rsi > 40:
        return None
    
    # need to be within 15% of a key level
    sma_lower_threshold = sma * 0.85
    sma_upper_threshold = sma * 1.15
    bol_lower_band_lower_threshold = bol_lower_band * 0.85
    bol_lower_band_upper_threshold = bol_lower_band * 1.15

    near_sma_level = sma_lower_threshold <= ticker_last_close <= sma_upper_threshold
    near_bol_level = bol_lower_band_lower_threshold <= ticker_last_close <= bol_lower_band_upper_threshold
    if near_sma_level or near_bol_level:
        sma_distance = (ticker_last_close - sma) / sma * 100
        bol_distance = (ticker_last_close - bol_lower_band) / bol_lower_band * 100
        positive_distances = [dist for dist in [sma_distance, bol_distance] if dist > 0]
        level_distance = min(positive_distances) if positive_distances else 0
        if level_distance == 0:
            return None
        
        return {
            'Ticker': ticker,
            'Price': round(ticker_last_close, 2),
            'SMA_20': round(sma, 2),
            'Lower Band': round(bol_last['Lower Band'].item(), 2),
            'Distance from key level%': round(level_distance, 2),
            'HV20% (Annualized)': round(hv20 * 100, 2)
        }
    
    return None
