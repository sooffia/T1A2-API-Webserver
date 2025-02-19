from datetime import datetime, date 
from flask import Blueprint, request 
from init import db 
from models.task import Task, task_schema, tasks_schema 
from models.category import Category 
from flask_jwt_extended import jwt_required, get_jwt_identity 
from controllers.comment_controller import comments_bp 
from controllers.task_tracking_controller import task_tracking_bp

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
tasks_bp.register_blueprint(comments_bp, url_prefix="/<int:task_id>/comments")
tasks_bp.register_blueprint(task_tracking_bp, url_prefix="/<int:task_id>/task_trackings")

# fetch all tasks - GET 
@tasks_bp.route("/")
def get_all_tasks():
    """
    Fetch all tasks and return them in descending order of due date.

    Returns:
        JSON: Serialized list of all tasks.
    """
    stmt = db.select(Task).order_by(Task.due_date.desc())
    tasks = db.session.scalars(stmt).all()
    return tasks_schema.dump(tasks)

@tasks_bp.route("/<int:task_id>")
def get_one_task(task_id):
    """
    Fetch a single task by its ID.

    Args:
        task_id (int): ID of the task to fetch.

    Returns:
        JSON: Serialized task data if found.
        dict: Error message if task not found.
    """
    stmt = db.select(Task).filter_by(id=task_id).options(db.joinedload(Task.task_tracking))
    task = db.session.scalar(stmt)
    if task:
        task_data = task_schema.dump(task)
        return task_data 
    else:
        return {"error": f"Task with id {task_id} not found"}, 404

# create a new task - POST
@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task(): 
    """
    Create a new task with the provided data.

    Returns:
        JSON: Serialized task data if created successfully.
        dict: Error message if category label is missing or invalid.
    """
    body_data = task_schema.load(request.get_json())

    # Extract and validate category label
    try:
        label = body_data["category"]["label"]
    except KeyError:
        return {"error": "Category label is required."}, 400

    category = Category.query.filter(Category.label.ilike(label.strip())).first()
    if not category:
        return {"error": f"Category with label '{label}' does not exist."}, 404
    
    # Create a new task model instance
    task = Task(
        title=body_data.get("title"),
        description=body_data.get("description"),
        due_date=date.today(),  
        priority=body_data.get("priority"), 
        category_id=category.id, 
        user_id=get_jwt_identity() 
    )
    db.session.add(task)
    db.session.commit()

    return task_schema.dump(task)

# delete task - DELETE 
@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_card(task_id):
    """
    Delete a task by its ID.

    Args:
        task_id (int): ID of the task to delete.

    Returns:
        dict: Success message if task deleted.
        dict: Error message if task not found or unauthorized.
    """
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)
    if task: 
        if str(task.user_id) != get_jwt_identity():
            return {"error": "It seems like you are not the owner of this task"}, 403
        
        db.session.delete(task)
        db.session.commit()
        return {"message": f"Task '{task.title}' deleted successfully"}
    else:
        return {"error": f"Task with id {task_id} not found"}, 404
    
# edit a task - PUT, PATCH 
@tasks_bp.route("/<int:task_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_task(task_id):
    """
    Update a task by its ID with the provided data.

    Args:
        task_id (int): ID of the task to update.

    Returns:
        JSON: Serialized task data if updated successfully.
        dict: Error message if task not found or unauthorized.
    """
    body_data = task_schema.load(request.get_json(), partial=True)
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)
    if task:
        if str(task.user_id) != get_jwt_identity():
            return {"error": "It seems like you are not the owner of this task"}, 403

        task.title = body_data.get("title") or task.title
        task.description = body_data.get("description") or task.description
        task.priority = body_data.get("priority") or task.priority 

        db.session.commit()
        return task_schema.dump(task)
    
    else: 
        return {"error": f"Task with id {task_id} not found"}, 404
    



















