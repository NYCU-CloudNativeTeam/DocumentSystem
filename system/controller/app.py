import os

from flask import Flask, redirect, request
from flask_admin import Admin
from dotenv import load_dotenv

from .document.routes import documents
from .auth.routes import auth
# from .notification.routes import notify
from .audit.routes import audit
from .account.routes import account
from .llm.routes import llm
from .googleAuth.routes import googleAuth
from .users.routes import users
from .config import Config
from model.base_model import db
from model.document_model import (
    Document,
    DocumentComment,
    DocumentPermission,
    DocumentPermissionType,
    DocumentStatus
)
from model.audit_model import Audit, AuditStatus
from model.user_model import User
from repo.audit_repo import AuditRepository
from repo.user_repo import UserRepository
from repo.document_repo import DocumentRepository

from flask_admin.contrib.sqla import ModelView
from model.user_model import User
from model.base_model import db

def init_dummy(db):
    user_repo = UserRepository()
    audit_repo = AuditRepository()
    document_repo = DocumentRepository()

    # Create some dummy users
    user1 = User(username='john_doe', name='John Doe', mail='john@example.com', google_id='google_id_1')
    user2 = User(username='jane_doe', name='Jane Doe', mail='jane@example.com', google_id='google_id_2')
    user3 = User(username='adam', name='Adam', mail='adam@example.com', google_id='google_id_3')

    for i in [
        user1,
        user2,
        user3
    ]:
        user_repo.add_user(i)

    # Create dummy audit statuses
    status1 = AuditStatus(name='Approved')
    status2 = AuditStatus(name='Rejected')
    status3 = AuditStatus(name='Pedding')
    status4 = AuditStatus(name='Not Sent')

    for i in [
        status1,
        status2,
        status3,
        status4
    ]:
        audit_repo.create_audit_status(i)

    documet_status_1 = DocumentStatus(name="Document status 1")
    documet_status_2 = DocumentStatus(name="Document status 2")
    documet_status_3 = DocumentStatus(name="Document status 3")

    for i in [
        documet_status_1,
        documet_status_2,
        documet_status_3
    ]:
        document_repo.create_document_status(i)

    # Create some dummy documents
    document1 = Document(uid='doc1', name='Document 1', body='Body of document 1', owner_id=user1.id, document_status_id=documet_status_1.id)
    document2 = Document(uid='doc2', name='Document 2', body='Body of document 2', owner_id=user2.id, document_status_id=documet_status_2.id)
    document3 = Document(uid='doc3', name='Document 3', body='Body of document 3', owner_id=user3.id, document_status_id=documet_status_3.id)

    for i in [
        document1,
        document2,
        document3,
    ]:
        document_repo.create_document(i)

    audit_status_1 = Audit(uid='audit1', document_id=document1.id, auditor_id=user1.id, audit_status_id=status1.id)
    audit_status_2 = Audit(uid='audit2', document_id=document2.id, auditor_id=user2.id, audit_status_id=status2.id)
    audit_status_3 = Audit(uid='audit3', document_id=document3.id, auditor_id=user3.id, audit_status_id=status3.id)
    audit_repo.create_audit(audit_status_1)
    audit_repo.create_audit(audit_status_2)
    audit_repo.create_audit(audit_status_3)

    document_permission_type1 = DocumentPermissionType(name='read')
    document_permission_type2 = DocumentPermissionType(name='write')
    document_repo.create_document_permission_type_not_exist(document_permission_type1)
    document_repo.create_document_permission_type_not_exist(document_permission_type2)

    document_permission1 = DocumentPermission(
        document_id=document1.id,
        user_id=user1.id,
        document_permission_type_id=document_permission_type1.id
    )
    document_permission2 = DocumentPermission(
        document_id=document1.id,
        user_id=user2.id,
        document_permission_type_id=document_permission_type2.id
    )
    document_permission3 = DocumentPermission(
        document_id=document1.id,
        user_id=user3.id,
        document_permission_type_id=document_permission_type2.id
    )
    document_repo.create_document_permission(document_permission1)
    document_repo.create_document_permission(document_permission2)
    document_repo.create_document_permission(document_permission3)

def create_app():
    load_dotenv()

    # create instance
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

    # Redirect AAA/ to AAA, instead the other way around (default)
    # https://stackoverflow.com/a/40365514/19378088
    app.url_map.strict_slashes = False
    @app.before_request
    def clear_trailing():
        rp = request.path
        if rp != '/' and rp.endswith('/'):
            return redirect(rp[:-1])

    # Config for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    app.config.from_object(Config)
    print(app.config)

    # Initialize the database with the app
    db.init_app(app)
    with app.app_context():
        # Creates all tables
        db.create_all()

        if app.config['DEBUG']:
            db.drop_all()
            db.create_all()
            init_dummy(db)

    # register document component
    # and also add prefix /document of URL
    app.register_blueprint(documents, url_prefix='/documents')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(auth, url_prefix='/auth')

    # register auth component
    # and also add prefix /auth of URL
    # app.register_blueprint(notify, url_prefix='/notify')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(audit, url_prefix='/audits')

    # register auth component
    # and also add prefix /account of URL
    app.register_blueprint(account, url_prefix='/account')

    # register auth component
    # and also add prefix /llm of URL
    app.register_blueprint(llm, url_prefix='/llm')

    # register auth component
    # and also add prefix /sign-in of URL
    app.register_blueprint(googleAuth, url_prefix='/sign-in')

    app.register_blueprint(users, url_prefix='/users')

    # import admin and register
    admin = Admin(app, url="/admin", name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(
        host = app.config['APP_HOST'],
        port = app.config['APP_PORT'],
        debug = app.config['DEBUG']
    )
