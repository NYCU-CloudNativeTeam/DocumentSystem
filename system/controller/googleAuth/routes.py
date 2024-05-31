from flask import Blueprint, redirect, jsonify, session, abort
from service.GoogleAuthService import GoogleAuthService

auth_service = GoogleAuthService()
googleAuth = Blueprint('sign-in', __name__)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@googleAuth.route("/", methods=["POST"], strict_slashes=False)
def get_session_inf():
    """
    retrun sign-in user information inculde id 、 username 、 name

    Example:
        Use the following curl command to call the endpoint:
            ```bash
            curl -i -X POST http://localhost:5000/sign-in \
            -H "Content-Type: application/json" \
            -d '{}'
            ```

    Args:
        JSON payload format:
            {
	            // Anything needed for the third-party account
            }


    Returns:
        Expected successful response format:
            {
                "id": "12345678",
	            "username": "albert123@gmail.com",
	            "name": "Albert",
            }
        
        Error response format:
            {
                "result": "Session is empty"
            }
    """
    if 'google_id' in session:
        return jsonify({"id": session['google_id'],
         "username": session['email'], 
         "name": session['name']}), 200
    return jsonify({"result": "Session is empty"}), 404

@googleAuth.route("/", methods=["GET"])
def login():
    authorization_url = auth_service.get_authorization_url()
    return redirect(authorization_url)

@googleAuth.route("/callback")
def callback():
    auth_service.fetch_token()
    auth_service.validate_state()
    auth_service.get_user_info()
    return redirect("/test_page_protected_area")

@googleAuth.route("/logout")
def logout():
    auth_service.clear_session()
    return redirect("/test_page/")

#Test use page(After logging in)
@googleAuth.route("/test_page_protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a><br>\
                information<br>\
                google_id : {session['google_id']}<br>\
                email : {session['email']}<br>\
                name : {session['name']}<br>\
                picture : {session['picture']}<br>"

#Test use page(Before logging in)
@googleAuth.route("/test_page")
def index():
    return "Hello World <a href='/sign-in/'><button>Login</button></a>"