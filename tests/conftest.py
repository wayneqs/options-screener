"""Pytest configuration."""
import pytest
from click.testing import CliRunner

@pytest.fixture
def runner():
    """Click CLI runner fixture."""
    return CliRunner()
