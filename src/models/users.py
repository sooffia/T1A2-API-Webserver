from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp

class User(db.Model):
    """Defines the User model with the following attributes:
    
    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): The user's name.
        email (str): Unique, required for user login.
        password (str): Encrypted password for user authentication.
        is_admin (bool): Flag indicating whether the user has admin privileges.
    
    Relationships:
        tasks: One-to-many relationship with the Task model.
        comments: One-to-many relationship with the Comment model.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    tasks = db.relationship('Task', back_populates='user', cascade="all, delete")
    comments = db.relationship('Comment', back_populates='user', cascade="all, delete")

class UserSchema(ma.Schema):
    """Schema for serializing and deserializing User objects."""
    
    email = fields.Email(
        validate=Regexp(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            error="Invalid email address format."
        )
    )
    password = fields.String(
        validate=Length(min=8, error="Password must be at least 8 characters long.")
    )
    tasks = fields.List(fields.Nested('TaskSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "tasks", "comments")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])