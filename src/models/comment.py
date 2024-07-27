from init import db, ma
from marshmallow import fields 

class Comment(db.Model): 
    """Defines the Comment model with the following attributes:
    
    Attributes:
        id (int): Primary key, auto-incremented.
        content (str): The content of the comment, not nullable.
        timestamp (datetime): The timestamp when the comment was created, not nullable.
        user_id (int): Foreign key referencing the User model, not nullable.
        task_id (int): Foreign key referencing the Task model, not nullable.
    
    Relationships:
        user: Many-to-one relationship with the User model.
        task: Many-to-one relationship with the Task model.
    """
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    task_idfi = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)

    user = db.relationship("User", back_populates ="comments")
    task = db.relationship("Task", back_populates="comments")

class CommentSchema(ma.Schema):
    """Schema for serializing and deserializing Comment objects."""
    
    user = fields.Nested("UserSchema", only=("name", "email"))
    task = fields.Nested("TaskSchema", exclude=["comments"])

    timestamp = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)

    class Meta: 
        fields = ("id", "content", "timestamp", "user", "task")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
