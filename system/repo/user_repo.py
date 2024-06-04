from typing import Optional, Dict, List
from model.user_model import User
from model.base_model import db
from model.document_model import Document

class UserRepository:
    def find_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user from the database by their username.

        This method searches the User model's database table for an entry
        that matches the provided username. If a matching user is found,
        it returns the User object. If no user is found, it returns None.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return User.query.filter_by(username=username).first()

    def find_user_by_id(self, user_id: int) -> Optional[User]:
        return User.query.get(user_id)

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

    def update_user_settings(self, user: User) -> None:
        """
        Commit changes of the user object to the database.

        Args:
            user (User): The user instance with updated fields that needs to be committed.

        Returns:
            None
        """
        db.session.commit()

    def find_user_by_name(self, name: str) -> User:
        """
        Find a user by their full name from the database.

        Args:
            name (str): The full name of the user to search for.

        Returns:
            User: The user object if found, otherwise None.
        """
        return User.query.filter_by(name=name).first()

    def find_user_by_id(self, user_id: str) -> User:
        """
        Find a user by their full name from the database.

        Args:
            name (str): The full name of the user to search for.

        Returns:
            User: The user object if found, otherwise None.
        """
        return User.query.filter_by(id=user_id).first()

    def find_users_by_search_text(self, search_text: str, document: Document, user: User) -> List[User]:
        """
        Find users by substring of their username from the database.

        Args:
            search_text (str): The search text for searching users' names and emails.

        Returns:
            List[User]: A list of User objects with the given name. Returns an empty list if no users are found.
        """
        return User.query.\
            filter(User.username.contains(search_text)).\
            filter(User.id != document.owner_id).\
            filter(User.id != user.id).\
            all()

    def find_user_by_google_id(self, google_id: str) -> Optional[User]:
        """
        Retrieve a user by their Google ID.

        Args:
            google_id (str): The Google ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return User.query.filter_by(google_id=google_id).first()
