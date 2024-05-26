from typing import Optional, Dict

from repo.user_repo import UserRepository
from model.user_model import User

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(
        self,
        username: str,
        name: str,
        mail: str,
        lock_session: Optional[str] = None,
        notification_flag: Optional[bool] = True, 
        third_party_info: Optional[str] = None
    ) -> User:
        """Create and store a new user.

        Args:
            username (str): User's username, must be unique.
            name (str): User's full name.
            mail (str): User's email, must be unique.
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
                'notification_flag': user.notification_flag
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
                'notification_flag': user.notification_flag
            }
        return None
