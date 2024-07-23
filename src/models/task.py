from init import db, ma 
from marshmallow import fields 

class Task(db.Model): 
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    due_date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    category = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="tasks")
    comments = db.relationship("Comment", back_populates="task", cascade="all, delete")

class TaskSchema(ma.Schema): 

    user = fields.Nested('UserSchema', only=("name", "email"))
    comments = fields.Nested("CommentSchema", exlcude=["task"])

    class Meta:
        fields = ("id","title", "description", "due_date", "status", "priority", "user", "comments")
        ordered = True 

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

