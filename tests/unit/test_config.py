"""Unit tests for config module."""

import pytest

from fastapi_ms_init.config import ProjectConfig


class TestProjectConfig:
    """Test ProjectConfig dataclass."""

    def test_project_config_minimal(self):
        """Test creating ProjectConfig with minimal required fields."""
        config = ProjectConfig(
            service_name="my-service",
            python_package_name="my_service"
        )
        assert config.service_name == "my-service"
        assert config.python_package_name == "my_service"

    def test_project_config_default_values(self):
        """Test that default values are set correctly."""
        config = ProjectConfig(
            service_name="my-service",
            python_package_name="my_service"
        )
        # Default values for US1 MVP
        assert config.use_postgres is False
        assert config.use_redis is False
        assert config.use_helm is False
        assert config.use_dagger is False
        assert config.use_otel is False  # MVP: False
        assert config.include_example_route is True
        assert config.include_background_task is False
        assert config.generate_docker_compose is True

    def test_project_config_custom_values(self):
        """Test creating ProjectConfig with custom values."""
        config = ProjectConfig(
            service_name="my-api",
            python_package_name="my_api",
            use_postgres=True,
            use_redis=True,
            include_example_route=False,
            generate_docker_compose=False,
        )
        assert config.service_name == "my-api"
        assert config.python_package_name == "my_api"
        assert config.use_postgres is True
        assert config.use_redis is True
        assert config.include_example_route is False
        assert config.generate_docker_compose is False

    def test_project_config_all_features_enabled(self):
        """Test ProjectConfig with all features enabled."""
        config = ProjectConfig(
            service_name="full-service",
            python_package_name="full_service",
            use_postgres=True,
            use_redis=True,
            use_helm=True,
            use_dagger=True,
            use_otel=True,
            include_example_route=True,
            include_background_task=True,
            generate_docker_compose=True,
        )
        assert config.use_postgres is True
        assert config.use_redis is True
        assert config.use_helm is True
        assert config.use_dagger is True
        assert config.use_otel is True
        assert config.include_example_route is True
        assert config.include_background_task is True
        assert config.generate_docker_compose is True

    def test_project_config_immutability(self):
        """Test that ProjectConfig is frozen (immutable)."""
        config = ProjectConfig(
            service_name="my-service",
            python_package_name="my_service"
        )
        # Dataclass frozen raises FrozenInstanceError (subclass of AttributeError)
        with pytest.raises((AttributeError, Exception)):
            config.service_name = "new-name"
