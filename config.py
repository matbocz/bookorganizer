import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # App configuration
    BOOKORGANIZER_ADMIN = os.environ.get('BOOKORGANIZER_ADMIN')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TEST_SECRET_KEY'

    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail configuration
    BOOKORGANIZER_MAIL_SUBJECT_PREFIX = '[Bookorganizer]'
    BOOKORGANIZER_MAIL_SENDER = 'Bookorganizer Admin <bookorganizer.matbocz@gmail.com>'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # App configuration
    DEBUG = True

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data-dev.sqlite')


class TestingConfig(Config):
    # App configuration
    TESTING = True

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
