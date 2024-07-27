from init import db, ma
from marshmallow import fields

class Category(db.Model):
    """Defines the Category model with the following attributes:
    
    Attributes:
        id (int): Primary key, auto-incremented.
        label (str): The name of the category.
    
    Relationships:
        tasks: One-to-many relationship with the Task model.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, nullable=False)

    tasks = db.relationship("Task", back_populates='category', cascade='all, delete')

class CategorySchema(ma.Schema):
    """Schema for serializing and deserializing Category objects."""

    tasks = fields.Nested('TaskSchema', many=True, exclude=['category'])

    class Meta:
        fields = ('id', 'label', 'tasks')
        ordered = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)