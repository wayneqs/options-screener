"""CLI interface using Click."""
import click
from rich.console import Console

from strategy_screener.core.ccs_screener import CCSScreener
from strategy_screener.core.ic_screener import ICScreener
from strategy_screener.core.pcs_screener import PCSScreener
from strategy_screener.utils.assets import Assets
from strategy_screener.utils.helpers import cached
from strategy_screener.utils.indicators import Indicators
from .config import config
import pandas as pd
from pathlib import Path

console = Console()

@click.group()
@click.version_option()
@click.option('--debug/--no-debug', default=None, help='Enable debug mode')
def cli(debug):
    if debug is not None:
        config.debug = debug
    
    # Validate configuration on startup
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        raise click.Abort()

@cached("get_tickers")
def get_tickers():
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    tickers = [s.replace('.', '-') for s in df['Symbol'].tolist()]
    tickers.append("HIMS")
    tickers.append("SOFI")
    tickers.append("HOOD")
    return tickers

@cli.command()
def screen():
    """Screen stocks."""
    # create output folder
    Path('output').mkdir(parents=True, exist_ok=True)

    tickers = get_tickers()
    console.print(f"Loaded {len(tickers)} tickers")

    data = Assets(tickers).download()

    Indicators(data).calculate_indicators()

    (ICScreener()
        .screen(data)
        .to_csv("output/iron-condors.csv", index=False))
    (PCSScreener()
        .screen(data)
        .to_csv("output/put-credit-spreads.csv", index=False))
    (CCSScreener()
        .screen(data)
        .to_csv("output/call-credit-spreads.csv", index=False))
    
    console.print(f"📊 Screening complete! Go and make some money.")

