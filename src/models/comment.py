from init import db, ma
from marshmallow import fields 

class Comment(db.Model): 
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Date) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)

    user = db.relationship("User", back_populates ="comments")
    task = db.relationship("Task", back_populates="comments")

class CommentSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=("name", "email"))
    task = fields.Nested("TaskSchema", exclude=["comments"])

    class meta: 
        fields = ("id", "message", "date", "user", "task")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

#check that the relationshiip match to what is in the erd 
