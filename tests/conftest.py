"""Pytest configuration and shared fixtures."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_service_name() -> str:
    """Return a valid service name for testing."""
    return "my-test-service"


@pytest.fixture
def sample_package_name() -> str:
    """Return a valid package name for testing."""
    return "my_test_service"
