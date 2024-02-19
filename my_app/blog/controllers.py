from flask import Blueprint, render_template, request

from my_app import db
# from .models import Post, Category, Tag
from . import models, forms # from my_app.blog import models


blogRoute = Blueprint('posts',__name__,url_prefix='/blog',)

@blogRoute.route('/')
def index():

    filterBlog = forms.FilterBlog(request.args)

    filterBlog.category.choices = [("","")] + [ (c.id, c.name) for c in models.Category.query.all() ]

    filterBlog.tag.choices = [ (t.id, t.name) for t in models.Tag.query.all() ]
    
    posts = db.session.query(models.Post)

    if filterBlog.search.data and filterBlog.search.data.strip():
        posts = posts.filter(models.Post.name.like('%'+filterBlog.search.data.strip()+'%'))

    if filterBlog.category.data:
         posts = posts.filter(models.Post.category_id==filterBlog.category.data)

    if filterBlog.tag.data:
        # posts = posts.join(models.post_tag).filter(models.post_tag.columns.tag_id == filterBlog.tag.data)
        posts = posts.join(models.post_tag).filter(models.post_tag.columns.tag_id.in_(filterBlog.tag.data))
        # posts = posts.join(models.post_tag).join(models.Tag).filter(models.Tag.id.in_(filterBlog.tag.data))

    # posts = posts.all()
    posts = posts.paginate(page=request.args.get('page', 1, type=int))

    return render_template('blog/index.html', filterBlog=filterBlog, posts=posts)
