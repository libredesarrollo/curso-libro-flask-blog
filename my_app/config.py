import os

from datetime import timedelta

ALLOWED_EXTENSIONS_FILES = { 'pdf', 'jpg', 'jpeg', 'gif', 'png' }
ALLOWED_EXTENSIONS_FILES_AVATAR = { 'jpg', 'jpeg', 'gif', 'png' }

def allowed_extensions_file(filename, list=ALLOWED_EXTENSIONS_FILES): #test.png
    # setting the rsplit:maxsplit parameter to 1, will return a list with 2 elements
    return '.' in filename and filename.lower().rsplit('.',1)[1] in list

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOAD_FOLDER=os.path.realpath('.') + '/my_app/assets/uploads'
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24)
    # Load secret key from environment variable. Provide a default for development.
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-default-dev-secret-key')

class ProdConfig(Config):
    DEBUG = False
    # Load the production database URI from an environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',  "sqlite:///" + os.path.join(basedir, "dev.db") )
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:____@mysql.railway.internal:3306/railway"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:____@shuttle.proxy.rlwy.net:17040/railway" # conectarse desde terminal a contenedor
    

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost:3306/flaskblog" 
    SECRET_KEY='SECRET_KEY'
    SECURITY_PASSWORD_SALT='5454d5sdsdsdsd121'
    # SQLALCHEMY_DATABASE_URI="mysql+pymysql://sail:password@localhost:3306/testing" 
    
class TestingConfig(DevConfig):
    WTF_CSRF_ENABLED=False
    BABEL_DEFAULT_LOCALE='en'