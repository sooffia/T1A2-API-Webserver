from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, nullable=False)

    tasks = db.relationship('Task', back_populates='category', cascade='all, delete')

class CategorySchema(ma.Schema):
    tasks = fields.Nested('TaskSchema', many=True, exclude=['category'])

    class Meta:
        fields = ('id', 'label', 'tasks')
        ordered = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)