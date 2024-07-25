from datetime import date 
from flask import Blueprint, request 
from init import db 
from models.task import Task, task_schema, tasks_schema 
from models.category import Category 
from flask_jwt_extended import jwt_required, get_jwt_identity 
from controllers.comment_controller import comments_bp 

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
tasks_bp.register_blueprint(comments_bp, url_prefix="/<int:task_id>/comments")

# fetch all tasks - GET 
@tasks_bp.route("/")
def get_all_tasks():
    stmt = db.select(Task).order_by(Task.due_date.desc())
    tasks = db.session.scalars(stmt)
    return tasks_schema.dump(tasks)

# fetch a single task _ GET 
@tasks_bp.route("/<int:task_id>")
def get_one_task(task_id):
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)
    if task:
        return task_schema.dump(task)
    else:
        return {"error": f"Task with id {task_id} not found"}, 404

# create a new task - POST
@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task(): 
    body_data = request.get_json()
    
    # Extract and validate category label
    label = body_data.get("label")
    if not label:
        return {"error": "Category label is required."}, 400

    # Look up category by label, making the query case-insensitive
    category = Category.query.filter(Category.label.ilike(label.strip())).first()
    if not category:
        return {"error": f"Category with label '{label}' does not exist."}, 404
    
    # a new task model instance
    task = Task(
        title=body_data.get("title"),
        description=body_data.get("description"),
        due_date=date.today(), 
        status=body_data.get("status"), 
        priority=body_data.get("priority"), 
        category_id=category.id, 
        user_id=get_jwt_identity() 
    )
    db.session.add(task)
    db.session.commit()
    return task_schema.dump(task)

# only able to see token if the email is admin but not with user...

# delete task - DELETE 
@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_card(task_id):
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)
    if task: 
        db.session.delete(task)
        db.session.commit()
        return {"message": f"Task '{task.title}' deleted successfully"}
    else:
        return {"error": f"Task with id {task_id} not found"}, 404
    
# edit a task - PUT, PATCH 
@tasks_bp.route("/<int:task_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_task(task_id):
    body_data = request.get_json()
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)
    if task:
        task.title = body_data.get("title") or task.title
        task.description = body_data.get("description") or task.description
        task.status = body_data.get("status") or task.status
        task.priority = body_data.get("priority") or task.priority 

        db.session.commit()
        return task_schema.dump(task)
    
    else: 
        return {"error": f"Task with id {task_id} not found"}, 404


















