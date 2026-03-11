"""
Blog Controllers (Blueprint)
=============================
Este módulo sólo se encarga de la capa HTTP:
  - Recibir la request
  - Delegar la lógica al servicio correspondiente
  - Renderizar la plantilla con los datos

Ninguna consulta a la BD ni regla de negocio vive aquí.
"""

from flask import Blueprint, render_template, request

from . import forms
from .services import post_service, category_service, tag_service


blogRoute = Blueprint('posts', __name__, url_prefix='/blog')


@blogRoute.route('/')
def index():
    """Lista paginada de posts con filtros opcionales."""

    filter_form = forms.FilterBlog(request.args)

    # Poblar choices desde los servicios (sin tocar la BD directamente aquí)
    filter_form.category.choices = [("", "")] + [
        (c.id, c.name) for c in category_service.get_all()
    ]
    filter_form.tag.choices = [
        (t.id, t.name) for t in tag_service.get_all()
    ]

    # Delegar la lógica de filtrado y paginación al servicio
    posts = post_service.get_filtered_posts(
        search=filter_form.search.data,
        category_id=filter_form.category.data,
        tag_ids=filter_form.tag.data,
        page=request.args.get('page', 1, type=int),
    )

    return render_template('blog/index.html', filterBlog=filter_form, posts=posts)
