from sqlalchemy.orm import relationship

from my_app import db
# tables

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, HiddenField
from wtforms.validators import InputRequired, ValidationError

def check_category2(form, field):
    res = Category.query.filter_by(name = field.data).first()
    if res:
        raise ValidationError("La categoría: %s ya fue tomada" % field.data)

def check_category2(form, field):
    res = Category.query.filter_by(name = field.data).first()
    if res:
        raise ValidationError("La categoría: %s ya fue tomada" % field.data)

def check_category(contain=True):
    def _check_category(form, field):
        print(form.id.data)
        if contain:
            res = Category.query.filter(Category.name.like("%"+field.data+"%")).first()
        else:
            res = Category.query.filter(Category.name.like(field.data)).first()

post_tag = db.Table('post_tag', 
                    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                    )

# models

class Category(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))

class Tag(db.Model):
    __tablename__='tags'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))

class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(255))
    content=db.Column(db.Text())

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', lazy='joined')

    tags = relationship(Tag, secondary=post_tag)

class PhoneForm(FlaskForm):
    phoneCode = StringField("Código teléfono")
    countryCode = StringField("Código país")
    phone = StringField("Teléfono")

class CategoryForm(PhoneForm):#, PhoneForm2
    name = StringField('Nombre', ) #validators=[InputRequired(), check_category(contain=False)]
    id = HiddenField('Id')
    recaptcha = RecaptchaField()
    #phonelist = FormField(PhoneForm)
    #phones = FieldList(FormField(PhoneForm))



    # tasks = relationship('Task', secondary=task_tag)
