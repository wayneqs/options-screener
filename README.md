# strategy-screener

A professional CLI application for screening options trading strategies.

## Installation

```bash
# Install in development mode
uv pip install -e .
```

## Usage

```bash
# Show help
strategy-screener --help

# Screen strategies for a symbol
strategy-screener screen --symbol AAPL

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
