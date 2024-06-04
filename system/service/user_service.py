from typing import Optional, Dict, List

from repo.user_repo import UserRepository
from repo.document_repo import DocumentRepository
from model.user_model import User

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.document_repository = DocumentRepository()

    def create_user(
        self,
        username: str,
        name: str,
        mail: str,
        google_id: str,
        lock_session: Optional[str] = None,
        notification_flag: Optional[bool] = True,
        third_party_info: Optional[str] = None
    ) -> User:
        """Create and store a new user.

        Args:
            username (str): User's username, must be unique.
            name (str): User's full name.
            mail (str): User's email, must be unique.
            google_id (str): User's Google ID.
            lock_session (Optional[str]): Session lock token, if any.
            notification_flag (Optional[bool]): Whether the user has notifications enabled.
            third_party_info (Optional[str]): Additional info related to third-party accounts.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If username or email already exists.
        """
        if self.user_repository.find_user_by_username(username) or \
           User.query.filter_by(mail=mail).first():
            raise ValueError("Username or email already exists.")

        new_user = User(
            username=username,
            name=name,
            mail=mail,
            google_id=google_id,
            lock_session=lock_session,
            notification_flag=notification_flag,
            third_party_info=third_party_info
        )
        return self.user_repository.add_user(new_user)

    def get_user_settings(self, username: str) -> Optional[Dict]:
        """
        Retrieve settings for a specified user by their username.

        This method fetches a user from the database using the username. If the user is found,
        it returns a dictionary with the user's current settings including their username, name,
        and notification flag status. If no user is found with the given username, the method returns None.

        Args:
            username (str): The username of the user whose settings are being retrieved.

        Returns:
            Optional[Dict]: A dictionary containing the user's settings if found; otherwise, None.
        """
        user = self.user_repository.find_user_by_username(username)
        if user:
            return {
                'username': user.username,
                'name': user.name,
                'emailNotifications': user.notification_flag
            }
        return None

    def update_user_settings(
        self,
        username: str,
        name: str,
        notification_flag: bool
    ) -> Optional[Dict]:
        """
        Update a user's settings based on the provided username.

        This method allows for updating the user's name and their
        notification preferences. It delegates the database update to
        the UserRepository and returns the updated user information.

        Args:
            username (str): The username of user whose settings to be updated.
            name (str): The new name to be updated.
            notification_flag (bool): The new state of the notification flag.

        Returns:
            Optional[Dict]: A dictionary containing the updated user information
                            if the user exists, otherwise None.
        """
        user = self.user_repository.find_user_by_username(username)
        if user:
            user.name = name
            user.notification_flag = notification_flag
            self.user_repository.update_user_settings(user)
            return {
                'username': user.username,
                'name': user.name,
                'emailNotifications': user.notification_flag
            }
        return None

    def find_user_by_name(self, name: str) -> Optional[User]:
        """
        Retrieve a user by their full name.

        This method queries the user repository to find a user based on the full name provided.
        If a matching user is found, it returns a dictionary containing key user details.
        If no user matches the provided name, it returns None.

        Args:
            name (str): The full name of the user to retrieve.

        Returns:
            Optional[Dict]: A dictionary containing user details if a user is found; otherwise, None.
            The dictionary includes the user's username, name, email, and notification settings.
        """
        user = self.user_repository.find_user_by_name(name)
        if user:
            return user
        return None

    def get_user_info_by_search_text(self, search_text: str, document_uid: str, user_id: int) -> List[dict]:
        """
        Retrieve detailed information about users by their name.

        Args:
            search_text (str): search text to search for in the database.

        Returns:
            List[dict]: A list of dictionaries containing user details such as name, email, and profile picture URL.
        """
        document = self.document_repository.get_document_by_uid(document_uid)
        user = self.user_repository.find_user_by_id(user_id)
        users = self.user_repository.find_users_by_search_text(search_text, document, user)
        return [{
                "name": user.name,
                "username": user.username,
                "profilePictureUrl": user.third_party_info
            } for user in users
        ]

    def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        """
        Retrieve a user by their Google ID.

        Args:
            google_id (str): The Google ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return self.user_repository.find_user_by_google_id(google_id)
