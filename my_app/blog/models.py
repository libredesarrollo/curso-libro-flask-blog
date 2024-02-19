from sqlalchemy.orm import relationship

from my_app import db
# tables

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



    # tasks = relationship('Task', secondary=task_tag)
