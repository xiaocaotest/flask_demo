
class Config:
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'SOME-RADOM-JWT-SECRET'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = <Production DB RUL>
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///./authors.db"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = <Testing DB URL>
    SQLALCHEMY_ECHO = False
