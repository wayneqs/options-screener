from .indicators import calculate_bollinger_bands, calculate_hv20
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
        by=["HV20% (Annualized)", "Distance from SMA%", ],
        key=lambda col: np.abs(col) if col.name == "Distance from SMA%" else col,
        ascending=[True, True]  # closest to SMA first, then highest HV20
    ).reset_index(drop=True)
    return results_df


def screen_name(ticker, ticker_df):
    """Screen stock based on various criteria."""
    bol_df = calculate_bollinger_bands(ticker_df)
    hv20_df = calculate_hv20(ticker_df)

    ticker_last = ticker_df.iloc[-1]
    bol_last = bol_df.iloc[-1]
    hv20_last = hv20_df.iloc[-1]

    ticker_last_close = ticker_last['Close'].item()
    sma = bol_last['SMA_20'].item()
    hv20 = hv20_last['HV20'].item()
    
    # let's look for names that are within 10% of the SMA
    lower = sma * 0.9
    upper = sma * 1.1

    if lower <= ticker_last_close <= upper:
        return {
            'Ticker': ticker,
            'Price': round(ticker_last_close, 2),
            'SMA_20': round(sma, 2),
            'Upper Band': round(bol_last['Upper Band'].item(), 2),
            'Lower Band': round(bol_last['Lower Band'].item(), 2),
            'Distance from SMA%': round((ticker_last_close - sma) / sma * 100, 2),
            'HV20% (Annualized)': round(hv20 * 100, 2)
        }
    
    return None
