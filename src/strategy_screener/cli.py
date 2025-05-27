"""CLI interface using Click."""
import click
from rich.console import Console
from .config import config
from .utils.assets import Assets
from .utils import icscreener
import pandas as pd
from pathlib import Path

console = Console()

@click.group()
@click.version_option()
@click.option('--debug/--no-debug', default=None, help='Enable debug mode')
def cli(debug):
    """Strategy Screener - A professional options trading CLI tool."""
    if debug is not None:
        config.debug = debug
    
    # Validate configuration on startup
    try:
        config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        raise click.Abort()

@cli.command()
def screen():
    """Screen stocks."""
    # create output folder
    Path('output').mkdir(parents=True, exist_ok=True)

    assets = Assets("data/assets")
    md = assets.get_market_data()
    names = icscreener.screen(md)
    names.to_csv("output/iron-condors.csv", index=False)
    console.print(f"📊 Found {len(names)} assets worth looking at")

@cli.command()
def config_info():
    """Show current configuration."""
    console.print("[bold]Current Configuration:[/bold]")
    console.print(f"Environment: {config.environment}")
    console.print(f"API Base URL: {config.api_base_url}")
    console.print(f"API Key: {'*' * len(config.api_key) if config.api_key else '[red]Not Set[/red]'}")
    console.print(f"Debug Mode: {config.debug}")
    console.print("Hello")
    
@cli.command()
def status():
    """Show application status."""
    console.print("[green]✓[/green] Strategy Screener is running!")
    console.print("Ready to find underlyings for the strategies.")
