import pytest
from flask import Flask
from flask.testing import FlaskClient
from model.base_model import db
from model.user_model import User
from controller.account.routes import account

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        user = User(username="albert123", name="Albert", mail="albert@example.com", notification_flag=True)
        db.session.add(user)
        db.session.commit()

    app.register_blueprint(account, url_prefix='/api/account')
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

# Test case for GET /account/settings with valid username
def test_get_account_settings_success(client: FlaskClient):
    response = client.get('/api/account/settings?username=albert123')
    assert response.status_code == 200
    assert response.json == {
        'username': 'albert123',
        'name': 'Albert',
        'notification_flag': True
    }

# Test case for GET /account/settings without providing a username
def test_get_account_settings_no_username(client: FlaskClient):
    response = client.get('/api/account/settings')
    assert response.status_code == 400
    assert response.json == {"error": "Username is required"}

# Test case for GET /account/settings with an unknown username
def test_get_account_settings_user_not_found(client: FlaskClient):
    response = client.get('/api/account/settings?username=unknown')
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

# Test case for PUT /account/settings with valid data
def test_update_account_settings_success(client: FlaskClient):
    response = client.put('/api/account/settings', json={
        'username': 'albert123',
        'name': 'Albert Updated',
        'emailNotifications': False
    })
    assert response.status_code == 200
    assert response.json == {
        'username': 'albert123',
        'name': 'Albert Updated',
        'notification_flag': False
    }

# Test case for PUT /account/settings with missing fields
def test_update_account_settings_missing_fields(client: FlaskClient):
    response = client.put('/api/account/settings', json={
        'username': 'albert123',
        'name': 'Albert Updated'
    })
    assert response.status_code == 400
    assert response.json == {"error": "All fields (username, name, emailNotifications) are required"}

# Test case for PUT /account/settings with an unknown username
def test_update_account_settings_user_not_found(client: FlaskClient):
    response = client.put('/api/account/settings', json={
        'username': 'unknown',
        'name': 'Unknown User',
        'emailNotifications': False
    })
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}
