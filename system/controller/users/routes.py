from flask import Blueprint, jsonify, request, current_app, session
from service.user_service import UserService

users = Blueprint('users', __name__)
user_service = UserService()

@users.route('/', methods=['GET'], strict_slashes=False)
def find_users():
    """
    Retrieve a list of users whose names contain the provided search text. The search is case-sensitive.

    Args:
        search-text (str): The search string used to filter user names and emails.

    Returns:
        JSON array of users matching the search criteria. Each user object contains the user's name,
        email, and optionally, their profile picture URL. If no users match the criteria,
        an empty list is returned. If the search text is not provided, returns a 400 error with
        a JSON error message.

    Example:
        * search user exist:
            ```bash
            $ curl -X GET 'http://127.0.0.1:8080/api/v1/users/?search-text=Adam'

            [
                {
                    "username": "adam123",
                    "name": "Adam",
                    "profilePictureUrl": null
                }
            ]
            ```
        * search user not exist:
            ```
            $ curl -X GET 'http://127.0.0.1:8080/api/v1/users/?search-text=IamNotExist'

            []
            ```
    """
    search_text = request.args.get('search-text')
    document_uid = request.args.get('document-uid')
    user_id = user_service.get_user_by_google_id(session['google_id']).id
    if not search_text:
        return jsonify({'error': 'Search text parameter is required'}), 400

    try:
        current_app.logger.info(f"Search user info by : {search_text}")
        users_info = user_service.get_user_info_by_search_text(search_text, document_uid, user_id)
        current_app.logger.info(f"Found {len(users_info)} data by : {search_text}")
        return jsonify(users_info), 200
    except Exception as e:
        current_app.logger.error(f"Error when search user name and email: {search_text}")
        current_app.logger.error(e)
        return jsonify({'error': 'An error occurred during the search'}), 500
