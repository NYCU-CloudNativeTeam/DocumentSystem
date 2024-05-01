import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from config import Config

app = Flask("Google Login App")

app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=app.config['REDIRECT_URL']
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    print("authorization_url",authorization_url)
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["iss"] = id_info.get("iss")
    session["azp"] = id_info.get("azp")
    session["aud"] = id_info.get("aud")
    session["sub"] = id_info.get("sub")
    session["email"] = id_info.get("email")
    session["email_verified"] = id_info.get("email_verified")
    session["at_hash"] = id_info.get("at_hash")
    session["name"] = id_info.get("name")
    session["picture"] = id_info.get("picture")
    session["given_name"] = id_info.get("given_name")
    session["family_name"] = id_info.get("family_name")
    session["locale"] = id_info.get("locale")
    session["iat"] = id_info.get("iat")
    session["exp"] = id_info.get("exp")
    session["jti"] = id_info.get("jti")
    session["alg"] = id_info.get("alg")
    session["kid"] = id_info.get("kid")
    session["typ"] = id_info.get("typ")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)