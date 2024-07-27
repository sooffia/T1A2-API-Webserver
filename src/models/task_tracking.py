from datetime import datetime 
from init import db, ma
from marshmallow import fields 

class TaskTracking(db.Model):
    __tablename__ = "task_trackings"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    estimated_hours = db.Column(db.Float, nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    actual_hours = db.Column(db.Float)

    task = db.relationship("Task", back_populates="task_tracking")

class TaskTrackingSchema(ma.Schema):
    task = fields.Nested("TaskSchema", exclude=["task_tracking"])
    
    started_at = fields.DateTime(format="%d/%m/%y %H:%M")
    finished_at = fields.DateTime(format="%d/%m/%y %H:%M")

    class Meta: 
        fields = ("id", "task", "estimated_hours", "actual_hours", "started_at", "finished_at")
        ordered = True 

task_tracking_schema = TaskTrackingSchema()
task_trackings_schema = TaskTrackingSchema(many=True)




