class Config(object):
    """parent config class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'questioner2-secret-key',
    JWT_SECRET_KEY = 'questioner2-jwt-secret-key',
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(Config):
    """prod config options"""
    DATABASE_URI = ""


class DevelopmentConfig(Config):
    """dev config options"""
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URI = ""


class TestingConfig(Config):
    """testing config options"""
    TESTING = True
    DATABASE_URI = ""


APP_CONFIG = {
        "prod": ProductionConfig,
        "dev": DevelopmentConfig,
        "testing": TestingConfig
    }
