import os, datetime

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
    #DO NOT use "DEBUG = True" in production environments
    DEBUG = False

    # Flask settings
    SECRET_KEY = 'bestspangeopfjieaorhjfoiawoicewafoajpoewfjpoaewjfoewjf'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    #JWT
    # app.config['JWT_AUTH_URL_RULE'] = '/login'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=1800)

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'designer@abbok.net'
    MAIL_PASSWORD = 'Abb0kMyAbb0k!'
    MAIL_DEFAULT_SENDER = '"MyApp" <designer@abbok.net>'

    # Flask-User settings
    USER_APP_NAME = "abbok design"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True       # Enable email authentication
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_ENABLE_MULTIPLE_EMAILS = False
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_INVITE_USER = False
    USER_ENABLE_USERNAME = True   # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "designer@abbok.net"
    USER_REQUIRE_RETYPE_PASSWORD = True

    USER_SHOW_EMAIL_DOES_NOT_EXIST = False
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False

    # 2 days (2*24*3600 seconds).
    USER_CONFIRM_EMAIL_EXPIRATION = 172800
    USER_RESET_PASSWORD_EXPIRATION = 172800
    USER_USER_SESSION_EXPIRATION = 3600

    USER_ENABLE_REGISTER = True
    USER_ENABLE_REMEMBER_ME = True

    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'
    USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
    USER_LOGIN_URL = '/user/sign-in'
    USER_LOGOUT_URL = '/user/sign-out'
    USER_MANAGE_EMAILS_URL = '/user/manage-emails'
    USER_REGISTER_URL = '/user/register'
