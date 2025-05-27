# strategy-screener

A CLI application for screening various underlyings to participate in options trading strategies.

## Installation

```bash
# Install in development mode
uv pip install -e .
```

## Usage

Make sure you have populated the tickers that you are interested in considering. The data files are located in the assets directory.

After running the screen, the output directory will be populated with CSV files for each strategy containing tickers that you might want to consider setting up trades on.

```bash
# Show help
strategy-screener --help

# Screen strategies for a symbol
strategy-screener screen

# Check status
strategy-screener status
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/
```
