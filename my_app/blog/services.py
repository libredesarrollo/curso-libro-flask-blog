"""
Blog Service Layer
==================
Toda la lógica de negocio relacionada con el blog vive aquí.
Los controladores (controllers.py) sólo orquestan HTTP; este módulo
se encarga de las consultas, filtros y reglas de dominio.
"""

from my_app import db
from my_app.blog import models


class PostService:
    """Servicio que encapsula todas las operaciones sobre Posts."""

    def get_filtered_posts(self, search: str = None, category_id=None, tag_ids=None, page: int = 1):
        """
        Devuelve un objeto de paginación con los posts que coinciden
        con los filtros proporcionados.

        Args:
            search     : texto libre para buscar en el nombre del post.
            category_id: id de categoría para filtrar.
            tag_ids    : lista de ids de etiquetas para filtrar.
            page       : número de página para la paginación.

        Returns:
            Pagination – objeto de SQLAlchemy con los posts filtrados.
        """
        query = db.session.query(models.Post)

        if search and search.strip():
            query = query.filter(models.Post.name.like(f'%{search.strip()}%'))

        if category_id:
            query = query.filter(models.Post.category_id == category_id)

        if tag_ids:
            query = (
                query
                .join(models.post_tag)
                .filter(models.post_tag.columns.tag_id.in_(tag_ids))
            )

        return query.paginate(page=page)


class CategoryService:
    """Servicio que encapsula operaciones sobre Categorías."""

    def get_all(self):
        """Retorna todas las categorías disponibles."""
        return models.Category.query.all()


class TagService:
    """Servicio que encapsula operaciones sobre Etiquetas."""

    def get_all(self):
        """Retorna todas las etiquetas disponibles."""
        return models.Tag.query.all()


# ── Instancias listas para usar en los controladores ──────────────────────────
post_service = PostService()
category_service = CategoryService()
tag_service = TagService()
