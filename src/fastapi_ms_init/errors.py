"""Custom exceptions for fastapi-ms-init."""


class ValidationError(Exception):
    """Base exception for validation errors."""

    pass


class InvalidServiceNameError(ValidationError):
    """Raised when a service name fails validation."""

    pass


class PackageNameConflictError(ValidationError):
    """Raised when a package name conflicts with Python stdlib."""

    pass


class OutputDirectoryExistsError(Exception):
    """Raised when the output directory already exists."""

    pass
