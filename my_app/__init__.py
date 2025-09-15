from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

from my_app.config import DevConfig, ProdConfig

app = Flask(__name__, static_folder='assets')





#configurations

# app.config.from_object(DevConfig)
app.config.from_object(ProdConfig)

#db
db=SQLAlchemy(app)
migrate = Migrate(app, db)

#seeder
seeder = FlaskSeeder()
seeder.init_app(app,db)

@app.route('/')
def hello_world(): # -> str
    return 'Hello Flask'



#blueprints
from my_app.blog.controllers import blogRoute
app.register_blueprint(blogRoute)

# def create_app():
#     app = Flask(__name__)

#     # app.config.from_pyfile('settings.py')

#     @app.route('/')
#     def index():
#         return '<h1>Hey There!</h1>'

#     return app