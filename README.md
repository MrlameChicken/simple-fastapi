# fastapi-ms-init

Production-ready FastAPI microservice generator CLI tool.

## Overview

`fastapi-ms-init` is a command-line tool that generates complete, production-ready FastAPI microservice projects in seconds. It scaffolds a best-practices project structure with tests, Docker support, and modern Python tooling.

## Features

- **Fast Setup**: Generate a complete FastAPI project in under 60 seconds
- **Production-Ready**: Includes Docker, tests, logging, and configuration
- **Modern Stack**: Python 3.11+, FastAPI, Pydantic settings, async support
- **Interactive CLI**: User-friendly prompts with colored output
- **Customizable**: Choose features like Postgres, Redis, Helm, and more

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd simple-fastapi

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### From PyPI (Future)

```bash
pip install fastapi-ms-init
```

## Usage

### Basic Usage

Generate a new FastAPI microservice:

```bash
fastapi-ms-init
```

The CLI will interactively prompt you for:
- Service name (e.g., `my-api-service`)
- Feature toggles (Postgres, Redis, example routes, etc.)
- Additional configuration options

### Generated Project Structure

```
my-api-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # API routes
│   └── core/
│       ├── __init__.py
│       ├── settings.py            # Pydantic settings
│       └── logging.py             # Structured logging
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest fixtures
│   ├── test_main.py               # Application tests
│   └── test_routes.py             # Route tests
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── .gitignore
```

### Running the Generated Service

```bash
cd my-api-service

# Install dependencies
pip install -e .

# Run with uvicorn
uvicorn app.main:app --reload

# Run tests
pytest

# Run with Docker
docker-compose up --build
```

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/unit/test_validators.py

# Run with verbose output
pytest -v
```

### Linting

```bash
# Run Ruff linting
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Project Requirements

- Python 3.11+
- 95%+ test coverage required
- All code must pass Ruff linting

## Project Structure (Generator Tool)

```
simple-fastapi/
├── src/
│   └── fastapi_ms_init/
│       ├── __init__.py
│       ├── cli.py                 # Typer CLI entrypoint
│       ├── generator.py           # Core generation logic
│       ├── validators.py          # Input validation
│       ├── config.py              # Configuration models
│       ├── errors.py              # Custom exceptions
│       └── templates/
│           └── base/              # Jinja2 templates
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── contract/                  # Contract tests
├── pyproject.toml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure 95%+ coverage and linting passes
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
