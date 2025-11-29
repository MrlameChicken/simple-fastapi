"""Integration test for minimal project generation."""

import subprocess

import pytest

from fastapi_ms_init.config import ProjectConfig
from fastapi_ms_init.generator import generate_project


class TestMinimalGeneration:
    """Integration test for minimal FastAPI project generation."""

    def test_generate_minimal_project_end_to_end(self, temp_dir):
        """Test generating a minimal project and verify it works."""
        config = ProjectConfig(
            service_name="test-service",
            python_package_name="test_service",
            use_postgres=False,
            use_redis=False,
            use_helm=False,
            use_dagger=False,
            use_otel=False,
            include_example_route=True,
            generate_docker_compose=True,
        )

        output_path = temp_dir / "test-service"

        # Generate the project
        generate_project(config, output_path)

        # Verify directory was created
        assert output_path.exists()
        assert output_path.is_dir()

        # Verify core files exist
        assert (output_path / "app" / "main.py").exists()
        assert (output_path / "tests" / "test_main.py").exists()
        assert (output_path / "Dockerfile").exists()
        assert (output_path / "pyproject.toml").exists()
        assert (output_path / "README.md").exists()

        # Verify docker-compose was generated (since enabled)
        assert (output_path / "docker-compose.yml").exists()

        # Verify core structure
        assert (output_path / "app" / "core" / "settings.py").exists()
        assert (output_path / "app" / "core" / "logging.py").exists()

    def test_generated_project_has_valid_python_syntax(self, temp_dir):
        """Test that all generated Python files have valid syntax."""
        config = ProjectConfig(
            service_name="syntax-test",
            python_package_name="syntax_test",
        )

        output_path = temp_dir / "syntax-test"
        generate_project(config, output_path)

        # Find all Python files
        python_files = list(output_path.rglob("*.py"))
        assert len(python_files) > 0, "Should generate at least some Python files"

        # Compile each file to check syntax
        for py_file in python_files:
            with open(py_file) as f:
                code = f.read()

            # This will raise SyntaxError if invalid
            compile(code, py_file, "exec")

    def test_generated_project_structure_matches_spec(self, temp_dir):
        """Test that generated project structure matches specification."""
        config = ProjectConfig(
            service_name="structure-test",
            python_package_name="structure_test",
        )

        output_path = temp_dir / "structure-test"
        generate_project(config, output_path)

        # Expected structure for US1 baseline
        expected_dirs = [
            "app",
            "app/api",
            "app/core",
            "tests",
        ]

        for dir_path in expected_dirs:
            full_path = output_path / dir_path
            assert full_path.exists(), f"Missing directory: {dir_path}"
            assert full_path.is_dir(), f"Not a directory: {dir_path}"

        # Expected files
        expected_files = [
            "app/__init__.py",
            "app/main.py",
            "app/api/__init__.py",
            "app/api/routes.py",
            "app/core/__init__.py",
            "app/core/settings.py",
            "app/core/logging.py",
            "tests/__init__.py",
            "tests/conftest.py",
            "tests/test_main.py",
            "tests/test_routes.py",
            "Dockerfile",
            "docker-compose.yml",
            "pyproject.toml",
            "README.md",
            ".gitignore",
        ]

        for file_path in expected_files:
            full_path = output_path / file_path
            assert full_path.exists(), f"Missing file: {file_path}"
            assert full_path.is_file(), f"Not a file: {file_path}"

    @pytest.mark.slow
    def test_generated_project_pytest_passes(self, temp_dir):
        """Test that generated project's tests pass (if pytest available)."""
        config = ProjectConfig(
            service_name="pytest-test",
            python_package_name="pytest_test",
        )

        output_path = temp_dir / "pytest-test"
        generate_project(config, output_path)

        # Try to run pytest in the generated project
        # This is a slow test, marked with @pytest.mark.slow
        try:
            result = subprocess.run(
                ["pytest", "-v"],
                cwd=output_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            # Tests should pass
            assert result.returncode == 0, f"Tests failed:\n{result.stdout}\n{result.stderr}"
        except FileNotFoundError:
            pytest.skip("pytest not available in PATH")
        except subprocess.TimeoutExpired:
            pytest.fail("pytest execution timed out")
