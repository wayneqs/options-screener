import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List
from rich.console import Console
import diskcache as dc

console = Console()

# Setup the cache directory
cache = dc.Cache("data/cache")

class BollingerScreener:
    """Screen stocks using Bollinger Bands."""

    def __init__(self, tickers: List[str]):
        self.tickers = tickers

    def get_stock_data(self, ticker, period="3mo", interval="1d", expire_secs=86400):
        """
        Fetches and caches stock data using diskcache.
        Args:
            ticker (str): Ticker symbol
            period (str): Period to fetch (e.g., '6mo')
            interval (str): Interval between data points (e.g., '1d')
            expire_secs (int): Cache expiry in seconds (default: 1 day)
        Returns:
            pd.DataFrame: Stock price data
        """
        cache_key = f"{ticker}_{period}_{interval}"
        
        if cache_key in cache:
            print(f"✅ Using cached data for {ticker}")
            return cache[cache_key]
        else:
            print(f"⬇️  Fetching new data for {ticker}")
            df = yf.download(ticker, period=period, interval=interval)
            cache.set(cache_key, df, expire=expire_secs)
            return df

    def run(self, target_file: str = "bollinger_scan_results.csv"):

        results = []

        for ticker in self.tickers:
            try:
                df = self.get_stock_data(ticker)

                if df.empty or len(df) < 20:
                    continue

                df['SMA20'] = df['Close'].rolling(window=20).mean()
                df['STDDEV'] = df['Close'].rolling(window=20).std()
                df['Upper'] = df['SMA20'] + 2 * df['STDDEV']
                df['Lower'] = df['SMA20'] - 2 * df['STDDEV']
                df['LogReturn'] = np.log(df['Close'] / df['Close'].shift(1))

                latest = df.iloc[-1]
                price = latest['Close'].item()
                sma = latest['SMA20'].item()
                hv20 = df['LogReturn'].rolling(window=20).std().iloc[-1].item() * np.sqrt(252)  # annualized

                if pd.isna(sma):
                    continue

                lower = sma * 0.9
                upper = sma * 1.1

                if lower <= price <= upper:
                    results.append({
                        'Ticker': ticker,
                        'Price': round(price, 2),
                        'SMA20': round(sma, 2),
                        'Upper Band': round(latest['Upper'].item(), 2),
                        'Lower Band': round(latest['Lower'].item(), 2),
                        'Distance from SMA%': round((price - sma) / sma * 100, 2),
                        'HV20 (Annualized)': round(hv20 * 100, 2)

                    })
            except Exception as e:
                console.print(f"Error for {ticker}: {e}")

        # Display sorted by proximity to basis
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(
            by=["Distance from SMA%", "HV20 (Annualized)"],
            key=lambda col: np.abs(col) if col.name == "Distance from SMA%" else col,
            ascending=[True, False]  # closest to SMA first, then highest HV20
        ).reset_index(drop=True)


        results_df.to_csv(target_file, index=False)
        console.print(f"📊 Bollinger Bands scan completed. Results saved to [bold]{target_file}[/bold].")