import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    """parent config class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY'),
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY'),
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    """dev config options"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """testing config options"""
    TESTING = True


APP_CONFIG = {
        "dev": DevelopmentConfig,
        "testing": TestingConfig
    }
