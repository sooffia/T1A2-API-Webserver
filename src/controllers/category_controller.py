from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.category import Category, category_schema, categories_schema
from models.task import Task, task_schema, tasks_schema

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

# Fetch tasks by category - GET
@categories_bp.route("/<int:category_id>/tasks", methods=["GET"])
def get_tasks_by_category(category_id):
    print(f"Fetching tasks for category_id: {category_id}")  # Debug print

    # Fetching tasks by category_id
    stmt = db.select(Task).filter_by(category_id=category_id)
    tasks = db.session.scalars(stmt).all()
    print(f"Tasks fetched: {tasks}")  # Debug print

    if tasks:
        response = jsonify(tasks_schema.dump(tasks))
        print(f"Response: {response.get_json()}")  # Debug print
        return response
    else:
        return {"error": f"No tasks found for category with id {category_id}"}, 404

# Fetch all categories - GET
@categories_bp.route("/", methods=["GET"])
def get_all_categories():
    stmt = db.select(Category).order_by(Category.label)
    categories = db.session.scalars(stmt).all()
    return jsonify(categories_schema.dump(categories))

# Fetch a single category - GET
@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_one_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        return jsonify(category_schema.dump(category))
    else:
        return {"error": f"Category with id {category_id} not found"}, 404

# Create a new category and assign it to a task - POST
@categories_bp.route("/tasks/<int:task_id>/categories", methods=["POST"])
@jwt_required()
def create_category(task_id):
    body_data = request.get_json()

    # Load the request data
    category_data = category_schema.load(body_data, partial=True)

    # Fetch the task by ID from the database
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)

    if not task:
        return {"error": f"Task with ID {task_id} not found"}, 404

    # Create and assign the category to the task
    category = Category(
        label=category_data.get("label")
    )
    db.session.add(category)
    db.session.commit()

    task.category_id = category.id
    db.session.commit()

    return task_schema.dump(task), 201

# Delete a category - DELETE
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        db.session.delete(category)
        db.session.commit()
        return {"message": f"Category '{category.label}' deleted successfully"}
    else:
        return {"error": f"Category with id {category_id} not found"}, 404
    
@categories_bp.route("/<int:category_id>", methods=["PATCH"])
@jwt_required()
def edit_category(category_id):
    body_data = request.get_json()

    # Fetch the category by ID from the database
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    if not category:
        return {"error": f"Category with id {category_id} not found"}, 404

    # Update the category label
    if 'label' in body_data:
        category.label = body_data['label']

    db.session.commit()

    # Fetch the updated category with related tasks
    updated_category = db.session.query(Category).filter_by(id=category_id).options(db.joinedload(Category.tasks)).one()
    
    return category_schema.dump(updated_category)













