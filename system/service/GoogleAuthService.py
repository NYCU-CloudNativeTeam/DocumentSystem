import os
import json
import pathlib
import requests
from flask import session, request, abort, current_app
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

class GoogleAuthService:
    def __init__(self):
        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secrets_json = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=self.client_secrets_json,
            scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
            redirect_uri="http://localhost/callback"
            #redirect_uri="https://redesigned-lamp-qgw7w95jg4r2xjjw-5000.app.github.dev/sign-in/callback"
        )

    def get_authorization_url(self):
        authorization_url, state = self.flow.authorization_url()
        session["state"] = state
        return authorization_url

    def fetch_token(self):
        self.flow.fetch_token(authorization_response=request.url)

    def validate_state(self):
        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

    def get_user_info(self):
        credentials = self.flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=self.GOOGLE_CLIENT_ID
        )

        user_info = {
            "google_id": id_info.get("sub"),
            "name": id_info.get("name"),
            "email": id_info.get("email"),
            "picture": id_info.get("picture")
        }
        session.update(user_info)
        return user_info

    def clear_session(self):
        session.clear()