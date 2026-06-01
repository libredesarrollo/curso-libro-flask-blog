from flask import Flask, redirect, url_for, render_template, request, session, flash

from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_seeder import FlaskSeeder # DEPRECATED!!
from flask_caching import Cache
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_babel import Babel

from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

from my_app.config import DevConfig, ProdConfig

app = Flask(__name__, static_folder='assets')

#************ flask caching
cache = Cache(app)

#configurations

if app.config['DEBUG']:
    app.config.from_object(DevConfig)
else:
    app.config.from_object(ProdConfig)

app.config.from_object(DevConfig)
app.config.from_object(ProdConfig)

#login
login_manager = LoginManager()
login_manager.init_app(app)

#jwt
jwt = JWTManager()
jwt.init_app(app)

#babel
def get_locale():
    # return 'es'

    if session['user'] and session['user']['lang']:
        return session['user']['lang']
    
    return request.accept_languages.best_match(['es','en'])

babel = Babel(app,locale_selector=get_locale)

def roles_required(*role_names):
    def wrapper(f):
        @wraps(f)   
        def wrap(*args, **kwargs):
            for r in role_names:
                if session['user']['roles'].find(r) < 0:
                    return "You do not have the role to perform this operation", 401
                
            return f(*args, **kwargs)
        return wrap
    return wrapper

#db
db=SQLAlchemy(app)
migrate = Migrate(app, db)

# Demo Mode DB Write Restriction
class DemoModeError(Exception):
    pass

from sqlalchemy import event

@event.listens_for(db.session, 'before_flush')
def block_database_writes(session, flush_context, instances):
    if app.config.get('DEMO_MODE', False):
        if session.new or session.dirty or session.deleted:
            raise DemoModeError("Las modificaciones a la base de datos están deshabilitadas en el modo demo.")

@app.errorhandler(DemoModeError)
def handle_demo_mode_error(error):
    flash(str(error), "danger")
    return redirect(request.referrer or url_for('hello_world'))

#seeder
# seeder = FlaskSeeder()
# seeder.init_app(app,db)

@app.route('/')
def hello_world(): # -> str    
    return render_template('welcome.html')



#blueprints
from my_app.blog import blogRoute
app.register_blueprint(blogRoute)

from my_app.celery_views import celery_bp
app.register_blueprint(celery_bp)

#restful
from my_app.api.task import TaskApi
from my_app.api.task_arg import TaskArgApi, TaskApiPagination, TaskArgUploadApi
from my_app.api.category_arg import CategoryArgApi
from my_app.api.tag_arg import TagArgApi
api = Api(app)
# api.add_resource(TaskApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskArgApi, '/api/task', '/api/task/<int:id>')
api.add_resource(TaskApiPagination, '/api/task/<int:page>/<int:per_page>')
api.add_resource(TaskArgUploadApi, '/api/task/upload/<int:id>')
api.add_resource(CategoryArgApi, '/api/category', '/api/category/<int:id>')
api.add_resource(TagArgApi, '/api/tag', '/api/tag/<int:id>')
# api.add_resource(TaskApiSave, '/api/task/<int:id>')

#blueprints
from my_app.auth.controllers import authRoute
from my_app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)

#create db
# with app.app_context():
#     db.create_all()
from my_app.tasks.models import Task
from my_app.auth.models import User
from sqlalchemy.sql.expression import or_
#route

# *** invoice
from my_app.invoice.productController import invoiceProductBp
from my_app.product.product import product
from my_app.product.category import category
from my_app.product.userController import userBp
#general
# import my_app.general.error_handle
#importar las vistas
app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(userBp)
app.register_blueprint(invoiceProductBp)


from my_app.util.template_filter import text_to_upper
app.add_template_filter(text_to_upper)

# def create_app():
#     app = Flask(__name__)

#     # app.config.from_pyfile('settings.py')

#     @app.route('/')
#     def index():
#         return '<h1>Hey There!</h1>'

#     return app