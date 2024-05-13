# service/user_service.py

from typing import Optional
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
