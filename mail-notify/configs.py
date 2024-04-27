from dotenv import get_key

class Config:
    TESTING = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'  # 預設為 localhost
    MAIL_PORT = 587  # 預設為 25
    MAIL_USE_TLS = True  # 預設為 False
    MAIL_USERNAME = get_key(".env", "MAIL_USERNAME")  # 預設為 None
    MAIL_PASSWORD = get_key(".env", "MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME  # 預設為 None，這個不設也可以

class TestingConfig(Config):
    TESTING = True
