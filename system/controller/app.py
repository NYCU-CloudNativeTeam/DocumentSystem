import os

from flask import Flask
from flask_admin import Admin
from dotenv import load_dotenv

from .document.routes import document
from .auth.routes import auth
from .notification.routes import notify
from .audit.routes import audit
from .account.routes import account
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

def create_app():
    load_dotenv()

    # create instance
    app = Flask(__name__)

    # Config for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    app.config.from_object(Config)
    print(app.config)

    # Initialize the database with the app
    db.init_app(app)
    with app.app_context():
        # Creates all tables
        db.create_all()

    # register document component
    # and also add prefix /document of URL
    app.register_blueprint(document, url_prefix='/api/document')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(auth, url_prefix='/api/auth')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(notify, url_prefix='/api/notify')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(audit, url_prefix='/api/audits')

    # register auth component
    # and also add prefix /account of URL
    app.register_blueprint(account, url_prefix='/api/account')

    # import admin and register
    admin = Admin(app, url="/api/admin", name='microblog', template_mode='bootstrap3')

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(
        host = app.config['APP_HOST'],
        port = app.config['APP_PORT'],
        debug = app.config['DEBUG']
    )