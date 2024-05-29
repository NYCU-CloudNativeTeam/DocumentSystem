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

@googleAuth.route("/login", methods=["GET"])
def login():
    authorization_url = auth_service.get_authorization_url()
    return redirect(authorization_url)

@googleAuth.route("/callback")
def callback():
    auth_service.fetch_token()
    auth_service.validate_state()
    auth_service.get_user_info()
    return redirect("/protected_area")

@googleAuth.route("/logout")
def logout():
    auth_service.clear_session()
    return redirect("/")

@googleAuth.route("/")
def index():
    return "Hello World <a href='/sign-in/login'><button>Login</button></a>"

@googleAuth.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a><br>\
                information<br>\
                google_id : {session['google_id']}<br>\
                iss : {session['iss']}<br>\
                azp : {session['azp']}<br>\
                aud : {session['aud']}<br>\
                sub : {session['sub']}<br>\
                email : {session['email']}<br>\
                email_verified : {session['email_verified']}<br>\
                at_hash : {session['at_hash']}<br>\
                name : {session['name']}<br>\
                picture : {session['picture']}<br>\
                given_name : {session['given_name']}<br>\
                family_name : {session['family_name']}<br>\
                locale : {session['locale']}<br>\
                iat : {session['iat']}<br>\
                exp : {session['exp']}<br>\
                jti : {session['jti']}<br>\
                alg : {session['alg']}<br>\
                kid : {session['kid']}<br>\
                typ : {session['typ']}<br>"
