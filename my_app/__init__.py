from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from my_app.config import DevConfig

app = Flask(__name__)

#configurations
app.config.from_object(DevConfig)

#db
db=SQLAlchemy(app)
migrate = Migrate(app, db)

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