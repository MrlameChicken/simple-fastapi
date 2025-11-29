"""CLI entrypoint for fastapi-ms-init."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from fastapi_ms_init.config import ProjectConfig
from fastapi_ms_init.errors import (
    InvalidServiceNameError,
    OutputDirectoryExistsError,
    PackageNameConflictError,
)
from fastapi_ms_init.generator import generate_project
from fastapi_ms_init.validators import (
    derive_package_name,
    is_valid_package_name,
    is_valid_service_name,
)

app = typer.Typer(
    name="fastapi-ms-init",
    help="Generate production-ready FastAPI microservice projects",
    add_completion=False,
)
console = Console()


def validate_service_name(service_name: str) -> str:
    """Validate service name and raise if invalid.

    Args:
        service_name: The service name to validate

    Returns:
        The validated service name

    Raises:
        InvalidServiceNameError: If service name is invalid
    """
    if not is_valid_service_name(service_name):
        raise InvalidServiceNameError(
            f"Invalid service name: '{service_name}'. "
            "Service name must be 3-50 characters, lowercase letters, "
            "numbers, and hyphens only. Cannot start/end with hyphen."
        )
    return service_name


@app.command()
def main():
    """Generate a new FastAPI microservice project."""
    console.print(
        Panel.fit(
            "[bold blue]FastAPI Microservice Generator[/bold blue]\n"
            "Create production-ready FastAPI projects in seconds",
            border_style="blue",
        )
    )

    # Prompt for service name with validation
    while True:
        service_name = typer.prompt(
            "\n[1/5] Service name (e.g., 'my-api-service')",
            default="my-service",
        )
        try:
            service_name = validate_service_name(service_name)
            break
        except InvalidServiceNameError as e:
            console.print(f"[red]✗[/red] {e}")
            console.print("[yellow]Please try again.[/yellow]")

    # Derive and validate package name
    package_name = derive_package_name(service_name)

    if not is_valid_package_name(package_name):
        console.print(
            f"[red]✗[/red] Package name '{package_name}' conflicts with Python stdlib"
        )
        raise PackageNameConflictError(
            f"Package name '{package_name}' conflicts with Python standard library"
        )

    console.print(f"[green]✓[/green] Python package name: [cyan]{package_name}[/cyan]")

    # Feature prompts for MVP (US1)
    console.print("\n[bold]Feature Selection[/bold]")

    use_postgres = typer.confirm(
        "[2/5] Include PostgreSQL support?",
        default=False,
    )

    use_redis = typer.confirm(
        "[3/5] Include Redis support?",
        default=False,
    )

    include_example_route = typer.confirm(
        "[4/5] Include example API route?",
        default=True,
    )

    generate_docker_compose = typer.confirm(
        "[5/5] Generate docker-compose.yml?",
        default=True,
    )

    # Create configuration
    config = ProjectConfig(
        service_name=service_name,
        python_package_name=package_name,
        use_postgres=use_postgres,
        use_redis=use_redis,
        use_helm=False,  # Not in US1
        use_dagger=False,  # Not in US1
        use_otel=False,  # Not in US1
        include_example_route=include_example_route,
        include_background_task=False,  # Not in US1
        generate_docker_compose=generate_docker_compose,
    )

    # Output path
    output_path = Path.cwd() / service_name

    # Generate project
    try:
        console.print("\n[bold]Generating project...[/bold]")

        generate_project(config, output_path)

        console.print("[green]✓[/green] Project generated successfully!\n")

        # Success message with next steps
        console.print(
            Panel.fit(
                f"[bold green]Success![/bold green]\n\n"
                f"Your FastAPI project has been created at: [cyan]{output_path}[/cyan]\n\n"
                f"[bold]Next steps:[/bold]\n"
                f"  1. cd {service_name}\n"
                f"  2. python -m venv .venv && .venv\\Scripts\\activate  (Windows)\n"
                f"     or source .venv/bin/activate  (Linux/Mac)\n"
                f"  3. pip install -e \".[dev]\"\n"
                f"  4. uvicorn app.main:app --reload\n\n"
                f"Visit http://localhost:8000/docs for API documentation!",
                border_style="green",
                title="🎉 Project Created",
            )
        )

    except OutputDirectoryExistsError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(code=1) from None
    except Exception as e:
        console.print(f"[red]✗[/red] Error generating project: {e}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
