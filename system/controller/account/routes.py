# controller/user_controller.py

from flask import Blueprint, request, jsonify
from service.user_service import UserService

account = Blueprint('account', __name__)
user_service = UserService()

@account.route('/', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user via POST request.
    
    Example:
        Expected JSON format:
        {
            "username": "sampleuser",
            "name": "Sample User",
            "mail": "user@example.com",
            "notification_flag": true,
            "third_party_info": "optional_info"
        }

        Using curl to call endpoint:
            ```bash
            curl -i -X POST http://localhost:5000/api/account \
            -H "Content-Type: application/json" \
            -d '{
                "username": "albert123",
                "name": "albert123",
                "mail": "alber@example.com",
                "notification_flag": true,
                "third_party_info": "optional_info"
                }'
            ```

    Returns:
        JSON response with the created user details or an error message.
    """
    data = request.json
    try:
        user = user_service.create_user(
            username=data['username'],
            name=data['name'],
            mail=data['mail'],
            lock_session=data.get('lock_session'),
            notification_flag=data.get('notification_flag', True),
            third_party_info=data.get('third_party_info')
        )
        return jsonify(user_id=user.id, username=user.username), 201
    except KeyError as e:
        return jsonify(error=f"Missing parameter: {str(e)}"), 400
    except ValueError as e:
        return jsonify(error=str(e)), 409

@account.route('/settings/<username>', methods=['GET'], strict_slashes=False)
def get_account_settings(username):
    """
    Retrieve settings for a specified user account identified by username.

    Example:
        Access this endpoint with the following curl command:
            ```bash
            curl -i -X GET http://localhost:5000/api/account/settings/albert123
            ```

    Args:
        username (str): Username of the user whose settings are to be retrieved.

    Returns:
        JSON response containing the user's settings if found, 
        or an error message if not found.
        The expected JSON format of a successful response is:
            {
                "username": "albert123",
                "name": "Albert",
                "emailNotifications": true
            }
    """
    settings = user_service.get_user_settings(username)
    if settings:
        return jsonify(settings), 200
    else:
        return jsonify({"error": "User not found"}), 404

@account.route('/settings', methods=['PUT'], strict_slashes=False)
def update_account_settings():
    """
    Update user account settings based on provided JSON data.

    Example:
        Use the following curl command to call the endpoint:
            ```bash
            curl -i -X PUT http://localhost:5000/api/account/settings \
            -H "Content-Type: application/json" \
            -d '{"username": "albert123", "name": "Albert Einstein", "emailNotifications": false}'
            ```

    Args:
        None directly, expects a JSON payload with username, name, and emailNotifications fields.

    Returns:
        JSON response with updated user details if successful or an error message if not found or data is missing. Expected successful response format:
            {
                "username": "albert123",
                "name": "Albert Einstein",
                "emailNotifications": false
            }
    """
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    notification_flag = data.get('emailNotifications')

    if not username or not name or notification_flag is None:
        return jsonify({"error": "All fields (username, name, emailNotifications) are required"}), 400

    updated_settings = user_service.update_user_settings(username, name, notification_flag)
    if updated_settings:
        return jsonify(updated_settings), 200
    else:
        return jsonify({"error": "User not found"}), 404
