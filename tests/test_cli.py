"""Test CLI interface."""
import pytest
from strategy_screener.cli import cli

def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Strategy Screener' in result.output

def test_status_command(runner):
    """Test status command."""
    result = runner.invoke(cli, ['status'])
    assert result.exit_code == 0
    assert 'running' in result.output
