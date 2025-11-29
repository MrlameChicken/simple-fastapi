"""Unit tests for CLI module."""

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from fastapi_ms_init.cli import app
from fastapi_ms_init.errors import InvalidServiceNameError, OutputDirectoryExistsError

runner = CliRunner()


class TestCLIBasicFunctionality:
    """Test basic CLI functionality."""

    @patch("fastapi_ms_init.cli.generate_project")
    @patch("fastapi_ms_init.cli.typer.confirm")
    @patch("fastapi_ms_init.cli.typer.prompt")
    def test_cli_minimal_generation(self, mock_prompt, mock_confirm, mock_generate):
        """Test CLI with minimal valid input."""
        # Mock user inputs
        mock_prompt.return_value = "my-test-service"  # service name
        mock_confirm.side_effect = [
            False,  # use_postgres
            False,  # use_redis
            True,   # include_example_route
            True,   # generate_docker_compose
        ]

        # Mock successful generation
        mock_generate.return_value = None

        result = runner.invoke(app, [])

        assert result.exit_code == 0
        mock_generate.assert_called_once()

    @patch("fastapi_ms_init.cli.generate_project")
    @patch("fastapi_ms_init.cli.typer.confirm")
    @patch("fastapi_ms_init.cli.typer.prompt")
    def test_cli_invalid_service_name(self, mock_prompt, mock_confirm, mock_generate):
        """Test CLI handles invalid service name."""
        # Mock invalid service name input
        mock_prompt.side_effect = [
            "Invalid_Name",  # invalid service name
            "my-test-service",  # valid retry
        ]
        mock_confirm.side_effect = [False, False, True, True]
        mock_generate.return_value = None

        runner.invoke(app, [])

        # Should prompt for retry on invalid name
        assert mock_prompt.call_count >= 2


class TestCLIValidation:
    """Test CLI input validation."""

    def test_service_name_validation_in_cli(self):
        """Test that CLI validates service names."""
        from fastapi_ms_init.cli import validate_service_name

        # Valid names
        assert validate_service_name("my-service") == "my-service"
        assert validate_service_name("api-123") == "api-123"

        # Invalid names raise error
        with pytest.raises(InvalidServiceNameError):
            validate_service_name("My_Service")

        with pytest.raises(InvalidServiceNameError):
            validate_service_name("ab")  # too short


class TestCLIErrorHandling:
    """Test CLI error handling."""

    @patch("fastapi_ms_init.cli.generate_project")
    @patch("fastapi_ms_init.cli.typer.confirm")
    @patch("fastapi_ms_init.cli.typer.prompt")
    def test_cli_handles_directory_exists_error(self, mock_prompt, mock_confirm, mock_generate):
        """Test CLI handles OutputDirectoryExistsError gracefully."""
        mock_prompt.return_value = "my-service"
        mock_confirm.side_effect = [False, False, True, True]
        mock_generate.side_effect = OutputDirectoryExistsError(
            "Directory 'my-service' already exists"
        )

        result = runner.invoke(app, [])

        # Should exit with error code
        assert result.exit_code != 0
        # Check that error message is present (normalize output)
        output_lower = result.output.lower()
        assert "exist" in output_lower or "directory" in output_lower
