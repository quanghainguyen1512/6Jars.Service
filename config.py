import os
import datetime

class Config(object):
    DEBUG = os.environ.get('ENV') == 'development'
    TESTING = False
    UPLOAD_FOLDER = '/uploaded_files'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    MONGO_URI = os.environ.get('DB')
    JWT_SECRET_KEY = os.environ.get('SECRET')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']