from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.task_tracking import TaskTracking, task_tracking_schema, task_trackings_schema
from models.task import Task

task_tracking_bp = Blueprint("task_trackings", __name__, url_prefix="/tasks/<int:task_id>/task_trackings")

def parse_date(date_input):
    if isinstance(date_input, datetime):
        return date_input
    return datetime.strptime(date_input, "%d/%m/%y %H:%M")

# Create a new task tracking record - POST
@task_tracking_bp.route("/", methods=["POST"])
@jwt_required()
def create_task_tracking(task_id):
    body_data = request.get_json()

    # Load the request data
    tracking_data = task_tracking_schema.load(body_data)

    # Fetch the task by ID from the database
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)

    if not task:
        return {"error": f"Task with ID {task_id} not found"}, 404

    # Parse datetime strings
    started_at = parse_date(tracking_data['started_at'])
    finished_at = parse_date(tracking_data.get('finished_at'))

    if not started_at or (tracking_data.get('finished_at') and not finished_at):
        return {"error": "Invalid date format. Use DD/MM/YY HH:MM"}, 400

    # Calculate actual_hours if finished_at is provided
    if finished_at:
        actual_hours = round((finished_at - started_at).total_seconds() / 3600, 2)
    else:
        actual_hours = None

    # Create the task tracking entry
    task_tracking = TaskTracking(
        task_id=task_id,
        estimated_hours=tracking_data.get("estimated_hours"),
        started_at=started_at,
        finished_at=finished_at,
        actual_hours=actual_hours
    )
    db.session.add(task_tracking)
    db.session.commit()

    return task_tracking_schema.dump(task_tracking), 201

# Update the task tracking record - PATCH
@task_tracking_bp.route("/<int:tracking_id>", methods=["PATCH"])
@jwt_required()
def update_task_tracking(task_id, tracking_id):
    body_data = request.get_json()

    # Validate and fetch the task tracking record by ID
    stmt = db.select(TaskTracking).filter_by(id=tracking_id, task_id=task_id)
    task_tracking = db.session.scalar(stmt)

    if not task_tracking:
        return {"error": f"Task tracking record with ID {tracking_id} not found for task {task_id}"}, 404

    # Update the start and/or finish time
    if "started_at" in body_data:
        task_tracking.started_at = parse_date(body_data["started_at"])
    if "finished_at" in body_data:
        task_tracking.finished_at = parse_date(body_data["finished_at"])
        # Calculate actual hours if both start and finish times are available
        if task_tracking.started_at and task_tracking.finished_at:
            task_tracking.actual_hours = round((task_tracking.finished_at - task_tracking.started_at).total_seconds() / 3600, 2)
    
     # Update the estimated_hours
    if "estimated_hours" in body_data:
        task_tracking.estimated_hours = body_data["estimated_hours"]

    db.session.commit()

    return task_tracking_schema.dump(task_tracking), 200

# Fetch all tracking records for a specific task - GET
@task_tracking_bp.route("/", methods=["GET"])
@jwt_required()
def get_task_trackings(task_id):
    stmt = db.select(TaskTracking).filter_by(task_id=task_id)
    task_trackings = db.session.scalars(stmt).all()

    if task_trackings:
        return jsonify(task_trackings_schema.dump(task_trackings))
    else:
        return {"error": f"No task tracking records found for task with id {task_id}"}, 404
    
# Delete the task tracking record - DELETE
@task_tracking_bp.route("/<int:tracking_id>", methods=["DELETE"])
@jwt_required()
def delete_task_tracking(task_id, tracking_id):
    # Fetch the task tracking record by ID and task ID
    stmt = db.select(TaskTracking).filter_by(id=tracking_id, task_id=task_id)
    task_tracking = db.session.scalar(stmt)

    if not task_tracking:
        return {"error": f"Task tracking record with ID {tracking_id} not found for task {task_id}"}, 404

    # Delete the task tracking record
    db.session.delete(task_tracking)
    db.session.commit()

    return {"message": f"Task tracking record with ID {tracking_id} deleted successfully"}, 200


