import yfinance as yf

from strategy_screener.utils.helpers import cached, cached_outside_market_hours

class Assets:
    """
    A class to represent a collection of assets.
    """

    def __init__(self, assets: list[str]):
        """
        Initializes the Assets instance with a list of asset names.

        :param assets: A list of asset names.
        """
        self.assets = assets

    def __str__(self):
        return f"Assets({self.assets})"

    def __repr__(self):
        return self.__str__()
    
    @cached("ticker")
    def download_asset(self, asset: str):
        """
        Downloads the data for a single asset from Yahoo Finance.

        :param asset: The name of the asset to download.
        :return: A DataFrame containing the asset's data.
        """
        try:
            return yf.download(asset, period="300d", interval="1d")
        except Exception as e:
            print(f"Error downloading {asset}: {e}")
            return None

    @cached("market_data")
    def download(self):
        """
        Downloads the asset data from Yahoo Finance.

        :return: A dictionary with asset names as keys and their data as values.
        """
        data = {}
        for asset in self.assets:
            try:
                data[asset] = yf.download(asset, period="300d", interval="1d")
            except Exception as e:
                print(f"Error downloading {asset}: {e}")
        return data