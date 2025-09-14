
class Config(object):
    pass

class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:twgYYhRdwyuEzAjuxuGYXeVvTdHulUUe@mysql.railway.internal:3306/railway" 

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://sail:password@localhost:3306/testing" 
    
    SECRET_KEY='SECRET_KEY'

class TestingConfig(DevConfig):
    WTF_CSRF_ENABLED=False