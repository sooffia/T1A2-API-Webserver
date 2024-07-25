from init import db, ma 
from marshmallow import fields 

# EDIT, ADD COMMENTS AND ERRORS!!

class Task(db.Model): 
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    due_date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="tasks")
    comments = db.relationship("Comment", back_populates="task", cascade="all, delete")
    category = db.relationship("Category", back_populates="tasks") 

class TaskSchema(ma.Schema): 
    user = fields.Nested('UserSchema', only=("name", "email"))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["task"]))
    category = fields.Nested("CategorySchema", only=("label",))

    class Meta:
        fields = ("id","title", "description", "due_date", "status", "priority", "user", "comments", "category")
        ordered = True 

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


    
    
    



