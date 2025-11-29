"""Contract tests for generated project structure."""


from fastapi_ms_init.config import ProjectConfig
from fastapi_ms_init.generator import generate_project


class TestGeneratedProjectContract:
    """Contract tests to ensure generated projects meet requirements."""

    def test_generated_project_has_health_endpoint(self, temp_dir):
        """Test that generated project includes a /health endpoint."""
        config = ProjectConfig(
            service_name="health-test",
            python_package_name="health_test",
        )

        output_path = temp_dir / "health-test"
        generate_project(config, output_path)

        # Read main.py and verify health endpoint exists
        main_py = output_path / "app" / "main.py"
        content = main_py.read_text()

        assert "/health" in content or "health" in content.lower()
        assert "FastAPI" in content

    def test_generated_project_has_settings(self, temp_dir):
        """Test that generated project includes Pydantic settings."""
        config = ProjectConfig(
            service_name="settings-test",
            python_package_name="settings_test",
        )

        output_path = temp_dir / "settings-test"
        generate_project(config, output_path)

        # Read settings.py
        settings_py = output_path / "app" / "core" / "settings.py"
        content = settings_py.read_text()

        assert "Settings" in content or "BaseSettings" in content
        assert "pydantic" in content.lower() or "BaseSettings" in content

    def test_generated_project_has_logging(self, temp_dir):
        """Test that generated project includes logging configuration."""
        config = ProjectConfig(
            service_name="logging-test",
            python_package_name="logging_test",
        )

        output_path = temp_dir / "logging-test"
        generate_project(config, output_path)

        # Read logging.py
        logging_py = output_path / "app" / "core" / "logging.py"
        content = logging_py.read_text()

        assert "logging" in content.lower()

    def test_generated_project_has_valid_dockerfile(self, temp_dir):
        """Test that generated Dockerfile is valid."""
        config = ProjectConfig(
            service_name="docker-test",
            python_package_name="docker_test",
        )

        output_path = temp_dir / "docker-test"
        generate_project(config, output_path)

        # Read Dockerfile
        dockerfile = output_path / "Dockerfile"
        content = dockerfile.read_text()

        assert "FROM python" in content
        assert "WORKDIR" in content
        assert "COPY" in content
        assert "uvicorn" in content.lower() or "CMD" in content

    def test_generated_project_has_valid_pyproject_toml(self, temp_dir):
        """Test that generated pyproject.toml has required dependencies."""
        config = ProjectConfig(
            service_name="deps-test",
            python_package_name="deps_test",
        )

        output_path = temp_dir / "deps-test"
        generate_project(config, output_path)

        # Read pyproject.toml
        pyproject = output_path / "pyproject.toml"
        content = pyproject.read_text()

        assert "fastapi" in content.lower()
        assert "uvicorn" in content.lower()
        assert "pydantic" in content.lower()
        assert "pytest" in content.lower()

    def test_generated_project_has_tests(self, temp_dir):
        """Test that generated project includes basic tests."""
        config = ProjectConfig(
            service_name="tests-test",
            python_package_name="tests_test",
        )

        output_path = temp_dir / "tests-test"
        generate_project(config, output_path)

        # Verify test files
        test_main = output_path / "tests" / "test_main.py"
        content = test_main.read_text()

        assert "def test_" in content
        assert "import" in content

    def test_generated_project_respects_example_route_flag(self, temp_dir):
        """Test that include_example_route flag is respected."""
        # With example route
        config_with = ProjectConfig(
            service_name="with-route",
            python_package_name="with_route",
            include_example_route=True,
        )

        output_with = temp_dir / "with-route"
        generate_project(config_with, output_with)

        routes_py = output_with / "app" / "api" / "routes.py"
        with_content = routes_py.read_text()

        # Should have example route
        assert "router" in with_content.lower() or "get" in with_content.lower()

        # Without example route
        config_without = ProjectConfig(
            service_name="without-route",
            python_package_name="without_route",
            include_example_route=False,
        )

        output_without = temp_dir / "without-route"
        generate_project(config_without, output_without)

        routes_py_without = output_without / "app" / "api" / "routes.py"
        without_content = routes_py_without.read_text()

        # Should be minimal or empty
        assert len(without_content) < len(with_content)

    def test_generated_project_respects_docker_compose_flag(self, temp_dir):
        """Test that generate_docker_compose flag is respected."""
        # With docker-compose
        config_with = ProjectConfig(
            service_name="with-compose",
            python_package_name="with_compose",
            generate_docker_compose=True,
        )

        output_with = temp_dir / "with-compose"
        generate_project(config_with, output_with)

        assert (output_with / "docker-compose.yml").exists()

        # Without docker-compose
        config_without = ProjectConfig(
            service_name="without-compose",
            python_package_name="without_compose",
            generate_docker_compose=False,
        )

        output_without = temp_dir / "without-compose"
        generate_project(config_without, output_without)

        assert not (output_without / "docker-compose.yml").exists()
