"""Input validation utilities for fastapi-ms-init."""

import re
import sys


def is_valid_service_name(name: str) -> bool:
    """Validate a service name.

    Rules:
    - Must be 3-50 characters long
    - Can only contain lowercase letters, numbers, and hyphens
    - Cannot start or end with a hyphen
    - Pattern: ^[a-z0-9-]+$

    Args:
        name: The service name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) < 3 or len(name) > 50:
        return False

    if name.startswith("-") or name.endswith("-"):
        return False

    # Only lowercase letters, numbers, and hyphens allowed
    pattern = r"^[a-z0-9-]+$"
    return bool(re.match(pattern, name))


def is_valid_package_name(name: str) -> bool:
    """Validate a Python package name.

    Rules:
    - Must be a valid Python identifier
    - Cannot conflict with Python stdlib modules
    - No hyphens allowed (use underscores)

    Args:
        name: The package name to validate

    Returns:
        True if valid, False otherwise
    """
    # Must be a valid Python identifier
    if not name.isidentifier():
        return False

    # Check for conflicts with Python stdlib
    if name in sys.stdlib_module_names:
        return False

    return True


def derive_package_name(service_name: str) -> str:
    """Derive a Python package name from a service name.

    Converts hyphens to underscores.

    Args:
        service_name: The service name (e.g., "my-service")

    Returns:
        The derived package name (e.g., "my_service")
    """
    return service_name.replace("-", "_")
