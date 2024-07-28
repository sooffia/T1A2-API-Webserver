from datetime import datetime 
from init import db, ma
from marshmallow import fields 

class TaskTracking(db.Model):
    """
    TaskTracking model for tracking task progress and time spent.

    Attributes:
        id (int): The primary key for the task tracking entry.
        task_id (int): Foreign key linking to the associated task.
        estimated_hours (float): Estimated hours required to complete the task.
        started_at (datetime): Timestamp indicating when the task was started.
        finished_at (datetime): Timestamp indicating when the task was finished.
        actual_hours (float): Actual hours spent on the task, calculated based on start and finish times.
    """
    __tablename__ = "task_trackings"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    estimated_hours = db.Column(db.Float, nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    actual_hours = db.Column(db.Float)

    task = db.relationship("Task", back_populates="task_tracking")

class TaskTrackingSchema(ma.Schema):
    """
    Schema for serializing and deserializing TaskTracking objects.
    
    Attributes:
        task (Nested): Nested TaskSchema excluding task_tracking to avoid recursion.
        started_at (DateTime): Formatted start timestamp.
        finished_at (DateTime): Formatted finish timestamp.
    """
    task = fields.Nested("TaskSchema", exclude=["task_tracking"])
    
    started_at = fields.DateTime(format="%d/%m/%y %H:%M")
    finished_at = fields.DateTime(format="%d/%m/%y %H:%M")

    class Meta: 
        fields = ("id", "task", "estimated_hours", "actual_hours", "started_at", "finished_at")
        ordered = True 

task_tracking_schema = TaskTrackingSchema()
task_trackings_schema = TaskTrackingSchema(many=True)




