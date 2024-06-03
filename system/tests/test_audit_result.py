import pytest
from flask import Flask
from flask.testing import FlaskClient
from datetime import datetime
from model.base_model import db
from model.user_model import User
from model.document_model import Document, DocumentStatus
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

        db.session.add(user)
        db.session.add(auditer)
        db.session.add(document)
        db.session.add(audit)
        db.session.add(audit_status)
        db.session.add(document2)
        db.session.add(audit2)
        db.session.add(audit_status2)
        db.session.commit()

    app.register_blueprint(account, url_prefix='/api/account')
    app.register_blueprint(documents, url_prefix='/api/documents')
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

# Test case for GET: /documents/[UID]/audit-result with valid document_uid
def test_get_audit_result_success(client: FlaskClient):
    response = client.get('/api/documents/abc123/audit-result')
    assert response.status_code == 200
    print(response.json)
    assert response.json == {
        "auditUid": "abc456",
        "documentUid": "abc123",
        "auditStatus": 2,
        "rejectedReason": "Insufficient references",
        "auditor": {
            "userId": 67890,
            "username": "auditorUsername",
            "name": "Auditor Name"
        },
  "auditedTime": "2024-05-28T00:00:00Z" 
}

# Test case for GET: /documents/[UID]/audit-result with no document_uid
def test_get_audit_result_with_error_document_uid(client: FlaskClient):
    response = client.get('/api/documents/error_document_uid/audit-result')
    assert response.status_code == 400
    assert response.json == {"error": "Audit record not found"}

# Test case for POST: /documents/[UID]/audit-result with valid audit-result
def test_post_audit_result_success(client: FlaskClient):
    data = {
        "auditStatus": 1,
        "rejectedReason": None
    }
    response = client.post(
        '/api/documents/bcd123/audit-result',
        json=data
    )
    assert response.status_code == 200
    assert response.json == {"message": "Audit status updated successfully"}
    
# Test case for POST: /documents/[UID]/audit-result with invalid audit-result
def test_post_audit_result_missing_rejectedReason(client: FlaskClient):
    data = {
        "auditStatus": 2
        # Missing rejectedReason
    }
    response = client.post(
        '/api/documents/abc123/audit-result',
        json=data
    )
    assert response.status_code == 400
    assert response.json == {"error": "Missing parameter: 'rejectedReason'"}

# Test case for POST: /documents/[UID]/audit-result with error document_uid
def test_post_audit_result_with_error_document_uid(client: FlaskClient):
    data = {
        "auditStatus": 1,
        "rejectedReason": None
    }
    response = client.post(
        '/api/documents/error_document_uid/audit-result',
        json=data
    )
    assert response.status_code == 400
    assert response.json == {"error": "Failed to update audit status"}
