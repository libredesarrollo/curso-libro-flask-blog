import os

class Config(object):
    # Load secret key from environment variable. Provide a default for development.
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-default-dev-secret-key')

class ProdConfig(Config):
    DEBUG = False
    # Load the production database URI from an environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', "PRO"  )
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:____@mysql.railway.internal:3306/railway"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:____@shuttle.proxy.rlwy.net:17040/railway" # conectarse desde terminal a contenedor
    

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost:3306/flaskblog" 
    # SQLALCHEMY_DATABASE_URI="mysql+pymysql://sail:password@localhost:3306/testing" 
    

class TestingConfig(DevConfig):
    WTF_CSRF_ENABLED=False