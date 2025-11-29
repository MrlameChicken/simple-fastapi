"""Unit tests for custom exceptions."""

import pytest

from fastapi_ms_init.errors import (
    InvalidServiceNameError,
    OutputDirectoryExistsError,
    PackageNameConflictError,
    ValidationError,
)


class TestValidationError:
    """Test base ValidationError exception."""

    def test_validation_error_with_message(self):
        """Test ValidationError with custom message."""
        error = ValidationError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert isinstance(error, Exception)

    def test_validation_error_inheritance(self):
        """Test that subclasses inherit from ValidationError."""
        assert issubclass(InvalidServiceNameError, ValidationError)
        assert issubclass(PackageNameConflictError, ValidationError)


class TestInvalidServiceNameError:
    """Test InvalidServiceNameError exception."""

    def test_invalid_service_name_error(self):
        """Test InvalidServiceNameError with custom message."""
        error = InvalidServiceNameError("Invalid name: My_Service")
        assert "Invalid name: My_Service" in str(error)
        assert isinstance(error, ValidationError)

    def test_invalid_service_name_error_can_be_raised(self):
        """Test that InvalidServiceNameError can be raised and caught."""
        with pytest.raises(InvalidServiceNameError) as exc_info:
            raise InvalidServiceNameError("Bad service name")
        assert "Bad service name" in str(exc_info.value)


class TestPackageNameConflictError:
    """Test PackageNameConflictError exception."""

    def test_package_name_conflict_error(self):
        """Test PackageNameConflictError with custom message."""
        error = PackageNameConflictError("Package 'os' conflicts with stdlib")
        assert "Package 'os' conflicts with stdlib" in str(error)
        assert isinstance(error, ValidationError)

    def test_package_name_conflict_error_can_be_raised(self):
        """Test that PackageNameConflictError can be raised and caught."""
        with pytest.raises(PackageNameConflictError) as exc_info:
            raise PackageNameConflictError("Stdlib conflict")
        assert "Stdlib conflict" in str(exc_info.value)


class TestOutputDirectoryExistsError:
    """Test OutputDirectoryExistsError exception."""

    def test_output_directory_exists_error(self):
        """Test OutputDirectoryExistsError with custom message."""
        error = OutputDirectoryExistsError("Directory /path/to/dir already exists")
        assert "Directory /path/to/dir already exists" in str(error)
        assert isinstance(error, Exception)

    def test_output_directory_exists_error_can_be_raised(self):
        """Test that OutputDirectoryExistsError can be raised and caught."""
        with pytest.raises(OutputDirectoryExistsError) as exc_info:
            raise OutputDirectoryExistsError("Directory exists")
        assert "Directory exists" in str(exc_info.value)

    def test_output_directory_exists_error_not_validation_error(self):
        """Test that OutputDirectoryExistsError is not a ValidationError."""
        error = OutputDirectoryExistsError("test")
        assert not isinstance(error, ValidationError)
        assert isinstance(error, Exception)
