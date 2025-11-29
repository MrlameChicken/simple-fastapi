"""Core project generation logic for fastapi-ms-init."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template

from fastapi_ms_init.config import ProjectConfig
from fastapi_ms_init.errors import OutputDirectoryExistsError


def check_output_directory(output_path: Path) -> None:
    """Check if output directory is valid for generation.

    Args:
        output_path: Path where project will be generated

    Raises:
        OutputDirectoryExistsError: If directory already exists
    """
    if output_path.exists():
        raise OutputDirectoryExistsError(
            f"Directory '{output_path}' already exists. "
            "Please choose a different location or remove the existing directory."
        )


def load_templates() -> Environment:
    """Load Jinja2 templates from package.

    Returns:
        Jinja2 Environment configured with template loader
    """
    # Get the templates directory relative to this file
    templates_dir = Path(__file__).parent / "templates" / "base"

    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_template(env: Environment, template_name: str, context: dict[str, Any]) -> str:
    """Render a template with given context.

    Args:
        env: Jinja2 Environment
        template_name: Name of template file
        context: Template context variables

    Returns:
        Rendered template string
    """
    template: Template = env.get_template(template_name)
    return template.render(**context)


def generate_project(config: ProjectConfig, output_path: Path) -> None:
    """Generate a FastAPI project based on configuration.

    Args:
        config: Project configuration
        output_path: Path where project will be generated

    Raises:
        OutputDirectoryExistsError: If output directory already exists
    """
    # Check output directory
    check_output_directory(output_path)

    # Load templates
    env = load_templates()

    # Template context
    context = {"config": config}

    # Create output directory structure
    output_path.mkdir(parents=True, exist_ok=True)

    # App structure
    app_dir = output_path / "app"
    app_dir.mkdir()
    (app_dir / "api").mkdir()
    (app_dir / "core").mkdir()

    # Tests structure
    tests_dir = output_path / "tests"
    tests_dir.mkdir()

    # Template file mappings: (template_name, output_path_relative)
    templates_to_render = [
        # App files
        ("app/__init__.py.j2", "app/__init__.py"),
        ("app/main.py.j2", "app/main.py"),
        ("app/api/__init__.py.j2", "app/api/__init__.py"),
        ("app/api/routes.py.j2", "app/api/routes.py"),
        ("app/core/__init__.py.j2", "app/core/__init__.py"),
        ("app/core/settings.py.j2", "app/core/settings.py"),
        ("app/core/logging.py.j2", "app/core/logging.py"),
        # Test files
        ("tests/__init__.py.j2", "tests/__init__.py"),
        ("tests/conftest.py.j2", "tests/conftest.py"),
        ("tests/test_main.py.j2", "tests/test_main.py"),
        ("tests/test_routes.py.j2", "tests/test_routes.py"),
        # Root files
        ("Dockerfile.j2", "Dockerfile"),
        ("pyproject.toml.j2", "pyproject.toml"),
        ("README.md.j2", "README.md"),
        (".gitignore.j2", ".gitignore"),
    ]

    # Conditionally add docker-compose
    if config.generate_docker_compose:
        templates_to_render.append(("docker-compose.yml.j2", "docker-compose.yml"))

    # Render and write all templates
    for template_name, output_file_path in templates_to_render:
        rendered_content = render_template(env, template_name, context)
        output_file = output_path / output_file_path
        output_file.write_text(rendered_content, encoding="utf-8")
