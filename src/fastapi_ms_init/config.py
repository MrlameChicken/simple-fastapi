"""Configuration models for fastapi-ms-init."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfig:
    """Configuration for generated FastAPI project.

    Attributes:
        service_name: Name of the service (e.g., "my-api-service")
        python_package_name: Python package name (e.g., "my_api_service")
        use_postgres: Include PostgreSQL support
        use_redis: Include Redis support
        use_helm: Include Helm chart
        use_dagger: Include Dagger CI/CD
        use_otel: Include OpenTelemetry
        include_example_route: Include example API route
        include_background_task: Include background task example
        generate_docker_compose: Generate docker-compose.yml
    """

    service_name: str
    python_package_name: str
    use_postgres: bool = False
    use_redis: bool = False
    use_helm: bool = False
    use_dagger: bool = False
    use_otel: bool = False
    include_example_route: bool = True
    include_background_task: bool = False
    generate_docker_compose: bool = True
