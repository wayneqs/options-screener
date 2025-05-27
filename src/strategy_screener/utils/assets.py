import yfinance as yf
import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.progress import track
from .helpers import cached_outside_market_hours
import pandas as pd

console = Console()

class Assets:
    """Handle reading JSON files safely."""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize with optional base path."""
        self.base_path = Path(base_path) if base_path else Path.cwd()
    
    def flatten_columns(self, df):
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        return df

    @cached_outside_market_hours("market_data")
    def download_market_data(self, ticker: str, period: str ="3mo", interval: str ="1d") -> Dict[str, Any]:
        """Download market data for a single ticker."""
        data = yf.download(ticker, period=period, interval=interval)
        #return self.flatten_columns(data)
        return data

    def get_market_data(self, tickers=None) -> Dict[str, Any]:
        """Download market data for a list of tickers or all if None."""
        if tickers is None:
            # If no tickers provided, read from JSON files in the base path
            file_paths = list(Path(self.base_path).glob("*.json"))
            
            tickers = []
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if not isinstance(data, list):
                            console.print(f"✗ Invalid data format in {file_path}: Expected a list")
                            continue
                        tickers.extend(data)
                except FileNotFoundError:
                    console.print(f"✗ File not found: {file_path}")
                    continue
                except json.JSONDecodeError as e:
                    console.print(f"✗ Invalid JSON in {file_path}: {e}")
                    continue
                except Exception as e:
                    console.print(f"✗ Error reading {file_path}: {e}")
                    continue

            return self.get_market_data(tickers)

        else:
            return {ticker: self.download_market_data(ticker) for ticker in track(tickers, description="Downloading market data...")}