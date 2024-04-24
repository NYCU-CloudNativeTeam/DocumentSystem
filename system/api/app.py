from flask import Flask
from flask_admin import Admin

from .document.routes import document
from .auth.routes import auth
from .notify.routes import notify
from .config import Config


def create_app():

    # create instance
    app = Flask(__name__)
    app.config.from_object(Config)
    print(app.config)

    # register document component
    # and also add prefix /document of URL
    app.register_blueprint(document, url_prefix='/api/document')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(auth, url_prefix='/api/auth')

    # register auth component
    # and also add prefix /auth of URL
    app.register_blueprint(notify, url_prefix='/api/notify')

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