"""Unit tests for validators module."""


from fastapi_ms_init.validators import (
    derive_package_name,
    is_valid_package_name,
    is_valid_service_name,
)


class TestServiceNameValidation:
    """Test service name validation."""

    def test_valid_service_names(self):
        """Test that valid service names are accepted."""
        valid_names = [
            "my-service",
            "api-gateway",
            "user-auth-service",
            "my-api-123",
            "service123",
        ]
        for name in valid_names:
            assert is_valid_service_name(name) is True, f"'{name}' should be valid"

    def test_invalid_service_name_special_chars(self):
        """Test that service names with invalid characters are rejected."""
        invalid_names = [
            "my_service",  # underscores not allowed
            "my.service",  # dots not allowed
            "my service",  # spaces not allowed
            "my@service",  # special chars not allowed
            "My-Service",  # uppercase not allowed
        ]
        for name in invalid_names:
            assert is_valid_service_name(name) is False, f"'{name}' should be invalid"

    def test_invalid_service_name_too_short(self):
        """Test that service names shorter than 3 characters are rejected."""
        assert is_valid_service_name("ab") is False
        assert is_valid_service_name("a") is False

    def test_invalid_service_name_too_long(self):
        """Test that service names longer than 50 characters are rejected."""
        long_name = "a" * 51
        assert is_valid_service_name(long_name) is False

    def test_invalid_service_name_starts_with_hyphen(self):
        """Test that service names starting with hyphen are rejected."""
        assert is_valid_service_name("-my-service") is False

    def test_invalid_service_name_ends_with_hyphen(self):
        """Test that service names ending with hyphen are rejected."""
        assert is_valid_service_name("my-service-") is False

    def test_valid_service_name_length_boundaries(self):
        """Test boundary conditions for service name length."""
        assert is_valid_service_name("abc") is True  # minimum length
        assert is_valid_service_name("a" * 50) is True  # maximum length


class TestPackageNameValidation:
    """Test package name validation."""

    def test_valid_package_names(self):
        """Test that valid Python package names are accepted."""
        valid_names = [
            "my_service",
            "api_gateway",
            "user_auth_service",
            "myapi123",
        ]
        for name in valid_names:
            assert is_valid_package_name(name) is True, f"'{name}' should be valid"

    def test_invalid_package_name_with_hyphen(self):
        """Test that package names with hyphens are rejected."""
        assert is_valid_package_name("my-service") is False

    def test_invalid_package_name_starts_with_number(self):
        """Test that package names starting with a number are rejected."""
        assert is_valid_package_name("123service") is False

    def test_invalid_package_name_stdlib_conflict(self):
        """Test that package names conflicting with stdlib are rejected."""
        stdlib_modules = ["os", "sys", "json", "re", "time"]
        for module in stdlib_modules:
            assert is_valid_package_name(module) is False, f"'{module}' should be rejected"

    def test_invalid_package_name_with_special_chars(self):
        """Test that package names with special characters are rejected."""
        invalid_names = [
            "my.service",
            "my service",
            "my@service",
        ]
        for name in invalid_names:
            assert is_valid_package_name(name) is False, f"'{name}' should be invalid"


class TestDerivePackageName:
    """Test package name derivation from service name."""

    def test_derive_package_name_simple(self):
        """Test basic hyphen to underscore conversion."""
        assert derive_package_name("my-service") == "my_service"
        assert derive_package_name("api-gateway") == "api_gateway"

    def test_derive_package_name_multiple_hyphens(self):
        """Test conversion with multiple hyphens."""
        assert derive_package_name("user-auth-service") == "user_auth_service"

    def test_derive_package_name_no_hyphens(self):
        """Test service name without hyphens."""
        assert derive_package_name("myservice") == "myservice"

    def test_derive_package_name_with_numbers(self):
        """Test service name with numbers."""
        assert derive_package_name("my-api-123") == "my_api_123"
