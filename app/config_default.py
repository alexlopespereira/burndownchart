import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = 'my precious'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    # Connect to the database
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:user@localhost/db'
    BURNDOWN_PATH = '/home/alex/Downloads/dev/burndownchart/burndownchart.py'

class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Connect to the database
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:user@localhost/db'

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:user@localhost/db'
    BURNDOWN_PATH = '/app/burndownchart.py'

