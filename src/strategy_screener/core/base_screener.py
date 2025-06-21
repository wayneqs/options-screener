from abc import ABC, abstractmethod
from rich.console import Console
import pandas as pd

console = Console()

class BaseScreener(ABC):
    
  def screen(self, data):
    """Screen stocks based on various criteria."""
    results = []
    for ticker, df in data.items():
        try:
            data = self._screen(ticker, df)
            if data:
                results.append(data)
        except Exception as e:
            console.print(f"Error processing {ticker}: {e}")

    results_df = pd.DataFrame(results)
    if not results_df.empty:
        results_df = results_df.sort_values(
            by=["HV Rank"],
            ascending=[False]
        ).reset_index(drop=True)
    
    return results_df

    @abstractmethod
    def _screen(self, ticker, data):
        pass