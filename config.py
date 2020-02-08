import os

FOLDER = os.getcwd() + '/static/images/avatars'


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///comments.sqlite3'
    SECRET_KEY = '_5#y2L"F4Q8z\n\xec]/'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = '/register'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', 'email')
    UPLOAD_FOLDER = FOLDER
