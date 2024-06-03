from flask import Flask
from flask_admin import Admin

app = Flask(__name__)
# app.register_blueprint(root_blueprint)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
