from typing import Optional
from model.user_model import User
from model.base_model import db

class UserRepository:
    def find_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        return User.query.filter_by(username=username).first()

    def add_user(self, user: User) -> User:
        """Add a new user to the database.

        Args:
            user (User): The user instance to be added.

        Returns:
            User: The newly added user instance.
        """
        db.session.add(user)
        db.session.commit()
        return user
