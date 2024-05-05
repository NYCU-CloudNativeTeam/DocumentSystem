from flask import Blueprint, jsonify


document = Blueprint('document', __name__)


@document.route('/')
def index():
    return jsonify({"message": "example of document route"}), 200