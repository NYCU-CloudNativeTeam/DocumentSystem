import pytest
from unittest.mock import MagicMock
from model.user_model import User
from model.base_model import db
from repo.user_repo import UserRepository

# Setup the application context and test client if using Flask or similar framework
@pytest.fixture
def user_repository():
    # Mock the SQLAlchemy session
    db.session = MagicMock()
    return UserRepository()

def test_find_user_by_username(user_repository):
    # Prepare the expected user
    expected_user = User(
        username = "testuser",
        name = "Test User",
        mail = "test@example.com"
    )

    # Setup a deep mock that simulates the chain of calls
    mock_query = MagicMock()
    mock_filter_by = MagicMock()
    mock_first = MagicMock(return_value=expected_user)

    mock_query.filter_by = MagicMock(return_value=mock_filter_by)
    mock_filter_by.first = mock_first

    # Replace the User.query with our mock
    User.query = mock_query

    # Execute the method
    result = user_repository.find_user_by_username("testuser")

    # Verify the result
    assert result == expected_user
    mock_query.filter_by.assert_called_once_with(username="testuser")
    mock_filter_by.first.assert_called_once()

def test_add_user(user_repository):
    # Prepare a user instance
    new_user = User(
        username = "newuser",
        name = "New User",
        mail = "new@example.com"
    )
    
    # Execute the method
    returned_user = user_repository.add_user(new_user)
    
    # Assertions to check correct behavior
    db.session.add.assert_called_once_with(new_user)
    db.session.commit.assert_called_once()
    assert returned_user == new_user

def test_update_user_settings(user_repository):
    user = User(
        username = "existinguser",
        name = "Existing User",
        mail = "existing@example.com"
    )

    # Execute the method
    user_repository.update_user_settings(user)

    # Check if commit was called
    db.session.commit.assert_called_once()

def test_find_user_by_id(user_repository):
    # Mock the query
    expected_user = User(
        id = 1,
        username = "userid",
        name = "User Name",
        mail = "user@example.com"
    )

    User.query.filter_by = MagicMock(
        return_value = MagicMock(
            first = MagicMock(
                return_value=expected_user)
            )
        )

    # Execute
    result = user_repository.find_user_by_id(1)

    # Verify
    assert result == expected_user
    User.query.filter_by.assert_called_once_with(id=1)
