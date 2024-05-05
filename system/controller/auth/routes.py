from flask import Blueprint, jsonify


# define auth as blueprint name
auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return jsonify({"message": "example of auth route"}), 200
