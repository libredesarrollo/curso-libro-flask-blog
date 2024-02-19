from flask_wtf import FlaskForm

from wtforms import StringField, SelectField, SelectMultipleField

class FilterBlog(FlaskForm):
    search=StringField("Search", render_kw={"class":"form-control"})
    category=SelectField("Category", render_kw={"class":"form-select"})
    # tag=SelectField("Tag", render_kw={"class":"form-select"})
    tag=SelectMultipleField("Tag", render_kw={"class":"form-select"})