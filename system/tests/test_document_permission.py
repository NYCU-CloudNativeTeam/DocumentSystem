import pytest
from flask import Flask
from flask.testing import FlaskClient
from datetime import datetime
from model.base_model import db
from model.user_model import User
from model.document_model import Document, DocumentStatus, DocumentPermission, DocumentPermissionType
from model.audit_model import Audit, AuditStatus
from controller.account.routes import account
from controller.document.routes import documents

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        user = User(
            id=56789, 
            username="normalUsername", 
            name="User Name", 
            mail="test@gmail.com", 
            lock_session="lock_session_1", 
            notification_flag=True, 
            third_party_info="third_party_info_1", 
            created_date=datetime(2024, 3, 20, 0, 0, 0), 
            updated_date=datetime(2024, 3, 20, 0, 0, 0)
        )
        auditer = User(
            id=67890, 
            username="auditorUsername", 
            name="Auditor Name", 
            mail="test2@gmail.com", 
            lock_session="lock_session_2", 
            notification_flag=True, 
            third_party_info="third_party_info_1", 
            created_date=datetime(2024, 3, 20, 0, 0, 0), 
            updated_date=datetime(2024, 3, 20, 0, 0, 0)
        )
        document = Document(
            id=2, 
            uid="abc123", 
            name="New Project", 
            body="test body", 
            owner_id=56789, 
            lock_session="lock_session_1", 
            document_status_id=1, 
            created_date=datetime(2024, 4, 27, 0, 0, 0), 
            updated_date=datetime(2024, 5, 27, 0, 0, 0)
        )
        audit = Audit(
            id=3, 
            uid="abc456", 
            document_id=2, 
            creator_id=56789, 
            audit_status_id=4, 
            rejected_reason="Insufficient references", 
            created_date=datetime(2024, 4, 27, 0, 0, 0), 
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )
        audit_status = AuditStatus(
            id=4, 
            name="Auditor Name", 
            audit_status_value=2, 
            created_date=datetime(2024, 5, 28, 0, 0, 0), 
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )

        document2 = Document(
            id=5, 
            uid="bcd123", 
            name="New Project2", 
            body="test body", 
            owner_id=56789, 
            lock_session="lock_session_1", 
            document_status_id=1, 
            created_date=datetime(2024, 4, 27, 0, 0, 0), 
            updated_date=datetime(2024, 5, 27, 0, 0, 0)
        )
        audit2 = Audit(
            id=6, 
            uid="abc567", 
            document_id=5, 
            creator_id=56789, 
            audit_status_id=7, 
            rejected_reason=None, 
            created_date=datetime(2024, 4, 27, 0, 0, 0), 
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )
        audit_status2 = AuditStatus(
            id=7, 
            name="Auditor Name", 
            audit_status_value=3, 
            created_date=datetime(2024, 5, 28, 0, 0, 0), 
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )

        permission_type_read = DocumentPermissionType(
            id=1,
            name="read",
            created_date=datetime(2024, 5, 28, 0, 0, 0),
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )
        permission_type_write = DocumentPermissionType(
            id=2,
            name="write",
            created_date=datetime(2024, 5, 28, 0, 0, 0),
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )

        document_permission1 = DocumentPermission(
            id=1,
            document_id=2,
            user_id=56789,
            document_permission_type_id=1,
            created_date=datetime(2024, 5, 28, 0, 0, 0),
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )
        document_permission2 = DocumentPermission(
            id=2,
            document_id=5,
            user_id=67890,
            document_permission_type_id=2,
            created_date=datetime(2024, 5, 28, 0, 0, 0),
            updated_date=datetime(2024, 5, 28, 0, 0, 0)
        )

        db.session.add(user)
        db.session.add(auditer)
        db.session.add(document)
        db.session.add(audit)
        db.session.add(audit_status)
        db.session.add(document2)
        db.session.add(audit2)
        db.session.add(audit_status2)
        db.session.add(permission_type_read)
        db.session.add(permission_type_write)
        db.session.add(document_permission1)
        db.session.add(document_permission2)
        db.session.commit()

    app.register_blueprint(account, url_prefix='/api/account')
    app.register_blueprint(documents, url_prefix='/api/documents')
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_get_document_permissions(client: FlaskClient):
    response = client.get('/api/documents/abc123/permissions')
    assert response.status_code == 200
    data = response.get_json()
    assert "permissions" in data
    assert len(data["permissions"]) == 1
    assert data["permissions"][0]["username"] == "normalUsername"

def test_update_document_permission(client: FlaskClient):
    response = client.put('/api/documents/abc123/permissions', json={
        "username": "normalUsername",
        "permissionType": 2
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Document permission updated successfully"

def test_update_document_permission_missing_fields(client: FlaskClient):
    response = client.put('/api/documents/abc123/permissions', json={
        "username": "normalUsername"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username and permissionType fields are required"

def test_update_document_name(client: FlaskClient):
    response = client.put('/api/documents/abc123/name', json={
        "name": "Updated Project Name"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Document name updated successfully"

    response = client.get('/api/documents/abc123')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Project Name"

def test_update_document_name_missing_fields(client: FlaskClient):
    response = client.put('/api/documents/abc123/name', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Name field is required"