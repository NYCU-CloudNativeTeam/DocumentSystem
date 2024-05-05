class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    DATABASE_URI = 'your_database_uri'

    # API setup
    APP_HOST = '0.0.0.0'
    APP_PORT = 5000

    # Redis
    REDIS_HOST = '0.0.0.0'
    REDIS_PORT = 6379