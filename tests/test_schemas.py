import pytest
from src.auth.schemas import UserCreate
from pydantic import ValidationError


def test_user_create_with_valid_email():
    # Create test data
    user = UserCreate(
        username="testuser",
        email="test@gmail.com",
        password="securepass123"
    )
    # Check created object
    assert user.username == "testuser"
    assert user.email == "test@gmail.com"


def test_user_create_with_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="testuser",
                   email="not-an-email",
                   password="securepass123")


# Check rejection of untrusted email domain
def test_user_create_with_untrusted_email_domain():
    with pytest.raises(ValueError, match="Email domain is not allowed"):
        UserCreate(username="testuser",
                   email="test@evil.com",
                   password="securepass123")
