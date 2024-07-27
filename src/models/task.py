from init import db, ma 
from marshmallow import fields, validates 
from marshmallow.validate import Length, And, Regexp, OneOf 
from marshmallow.exceptions import ValidationError 

# Define valid priorities as a constant
VALID_PRIORITIES = ("Low", "Medium", "High", "Critical", "Routine", "Optional") 

class Task(db.Model): 
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    due_date = db.Column(db.Date)
    priority = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="tasks")
    comments = db.relationship("Comment", back_populates="task", cascade="all, delete")
    category = db.relationship("Category", back_populates="tasks")
    task_tracking = db.relationship("TaskTracking", back_populates="task", uselist=False) 

class TaskSchema(ma.Schema): 
    user = fields.Nested('UserSchema', only=("name", "email"))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["task"]))
    category = fields.Nested("CategorySchema", only=("label",))

    title = fields.String(
        required=True, 
        validate=And(
            Length(min=2, error="Title must be at least two characters long"), 
            Regexp('^[A-Za-z0-9 ]+$', error="Title must have alphanumerics characters only")
        )
    )

    priority = fields.String(validate=OneOf(VALID_PRIORITIES, error="Invalid Priority"))

    class Meta:
        fields = ("id","title", "description", "due_date", "priority", "user", "comments", "category","task_tracking")
        ordered = True 

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


    
    
    



