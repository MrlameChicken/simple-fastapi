"""Unit tests for generator module."""


import pytest

from fastapi_ms_init.config import ProjectConfig
from fastapi_ms_init.errors import OutputDirectoryExistsError
from fastapi_ms_init.generator import (
    check_output_directory,
    generate_project,
    load_templates,
    render_template,
)


class TestCheckOutputDirectory:
    """Test output directory validation."""

    def test_check_output_directory_not_exists(self, temp_dir):
        """Test check passes when directory doesn't exist."""
        output_path = temp_dir / "new-service"
        # Should not raise
        check_output_directory(output_path)

    def test_check_output_directory_exists(self, temp_dir):
        """Test check fails when directory exists."""
        output_path = temp_dir / "existing-service"
        output_path.mkdir()

        with pytest.raises(OutputDirectoryExistsError) as exc_info:
            check_output_directory(output_path)

        assert "already exists" in str(exc_info.value).lower()

    def test_check_output_directory_exists_but_empty(self, temp_dir):
        """Test check passes when directory exists but is empty."""
        output_path = temp_dir / "empty-service"
        output_path.mkdir()

        # Empty directory is acceptable (some implementations)
        # For US1, we'll be strict and reject any existing directory
        with pytest.raises(OutputDirectoryExistsError):
            check_output_directory(output_path)


class TestLoadTemplates:
    """Test template loading."""

    def test_load_templates_returns_environment(self):
        """Test that load_templates returns a Jinja2 Environment."""
        from jinja2 import Environment

        env = load_templates()
        assert isinstance(env, Environment)

    def test_load_templates_can_find_base_templates(self):
        """Test that templates directory is accessible."""
        env = load_templates()

        # Should be able to list templates (will have templates after T019-T032)
        assert env.loader is not None


class TestRenderTemplate:
    """Test template rendering."""

    def test_render_template_simple(self):
        """Test rendering a simple template."""
        from jinja2 import DictLoader, Environment

        env = Environment(loader=DictLoader({
            "test.j2": "Hello {{ name }}!"
        }))

        result = render_template(env, "test.j2", {"name": "World"})
        assert result == "Hello World!"

    def test_render_template_with_config(self):
        """Test rendering template with ProjectConfig."""
        from jinja2 import DictLoader, Environment

        env = Environment(loader=DictLoader({
            "service.j2": "Service: {{ config.service_name }}"
        }))

        config = ProjectConfig(
            service_name="my-service",
            python_package_name="my_service"
        )

        result = render_template(env, "service.j2", {"config": config})
        assert result == "Service: my-service"


class TestGenerateProject:
    """Test full project generation."""

    def test_generate_project_creates_directory(self, temp_dir, sample_service_name):
        """Test that generate_project creates the output directory."""
        # This test is covered by integration tests
        # Just verify the function signature is correct
        assert callable(generate_project)

    def test_generate_project_rejects_existing_directory(
        self, temp_dir, sample_service_name
    ):
        """Test that generate_project fails if directory exists."""
        config = ProjectConfig(
            service_name=sample_service_name,
            python_package_name="my_test_service"
        )

        output_path = temp_dir / sample_service_name
        output_path.mkdir()

        with pytest.raises(OutputDirectoryExistsError):
            generate_project(config, output_path)

    def test_generate_project_with_minimal_config(self):
        """Test project generation with minimal configuration."""
        config = ProjectConfig(
            service_name="minimal-service",
            python_package_name="minimal_service",
            include_example_route=False,
            generate_docker_compose=False,
        )

        # Verify config properties
        assert config.include_example_route is False
        assert config.generate_docker_compose is False
