from flask import Blueprint

# from .models import Post, Category, Tag
from . import models # from my_app.blog import models

blogRoute = Blueprint('posts',__name__,url_prefix='/blog',)

@blogRoute.route('/')
def index():
    pass
