from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.category import Category, category_schema, categories_schema
from models.task import Task, task_schema, tasks_schema
from sqlalchemy.exc import SQLAlchemyError

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

# Fetch tasks by category - GET
@categories_bp.route("/<int:category_id>/tasks", methods=["GET"])
def get_tasks_by_category(category_id):
    """Fetch tasks for a specific category.
    This endpoint allows users to fetch tasks belonging to a specific category.

    Args:
        category_id (int): The ID of the category whose tasks will be fetched.

    Returns:
        JSON: A list of tasks in the specified category or an error message.
        200: Tasks fetched successfully.
        404: No tasks found for the specified category.
        500: Internal server error.
    """ 
    try:
        print(f"Fetching tasks for category_id: {category_id}")  # Debug print

        # Fetching tasks by category_id
        stmt = db.select(Task).filter_by(category_id=category_id)
        tasks = db.session.scalars(stmt).all()

        if tasks:
            response = jsonify(tasks_schema.dump(tasks))
            return response 
        else:
            return {"error": f"No tasks found for category with id {category_id}"}, 404

    except Exception:
        return {"error": "An unexpected error occurred"}, 500

# Fetch all categories - GET
@categories_bp.route("/", methods=["GET"])
def get_all_categories():
    """Fetch all categories.
    This endpoint allows users to fetch all categories.

    Returns:
        JSON: A list of all categories or an error message.
        200: Categories fetched successfully.
        500: Internal server error.
    """
    try:
        stmt = db.select(Category).order_by(Category.label)
        categories = db.session.scalars(stmt).all()
        return jsonify(categories_schema.dump(categories))
    
    except Exception:
        return {"error": "An unexpected error occurred while fetching categories"}, 500

# Fetch a single category - GET
@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_one_category(category_id):
    """Fetch a single category by its ID.
    This endpoint allows users to fetch a category by its ID.

    Args:
        category_id (int): The ID of the category to be fetched.

    Returns:
        JSON: The category data or an error message.
        200: Category fetched successfully.
        404: Category not found.
        500: Internal server error.
    """
    try: 
        stmt = db.select(Category).filter_by(id=category_id)
        category = db.session.scalar(stmt)
        if category:
            return jsonify(category_schema.dump(category))
        else:
            return {"error": f"Category with id {category_id} not found"}, 404
        
    except Exception:
        return {"error": "An unexpected error occurred while fetching the category"}, 500

# Create a new category and assign it to a task - POST
@categories_bp.route("/tasks/<int:task_id>/categories", methods=["POST"])
@jwt_required()
def create_category(task_id):
    """Create a new category and assign it to a task.
    This endpoint allows an authenticated user to create a new category and assign it to a task.

    Args:
        task_id (int): The ID of the task to which the category will be assigned.

    Request JSON Body:
        label (str): The name of the category.

    Returns:
        JSON: The created category data or an error message.
        201: Category created successfully.
        400: Validation error in the request data.
        404: Task not found.
        500: Internal server error.
    """
    body_data = request.get_json()

    try: 
        # Load the request data
        category_data = category_schema.load(body_data, partial=True)

        # Fetch the task by ID from the database
        stmt = db.select(Task).filter_by(id=task_id)
        task = db.session.scalar(stmt)

        if not task:
            return {"error": f"Task with ID {task_id} not found"}, 404

        # Check for unique label
        existing_category = Category.query.filter_by(label=category_data.get("label")).first()
        if existing_category:
            return {"error": "A category with this label already exists."}, 400

        # Create and assign the category to the task
        category = Category(
            label=category_data.get("label")
        )
        db.session.add(category)
        db.session.commit()

        task.category_id = category.id
        db.session.commit()

        return task_schema.dump(task), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while creating the category"}, 500

# Delete a category - DELETE
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    """Delete a category by its ID.
    This endpoint allows an authenticated user to delete a category.

    Args:
        category_id (int): The ID of the category to be deleted.

    Returns:
        JSON: Success message or error message.
        200: Category deleted successfully.
        404: Category not found.
        500: Internal server error.
    """
    try:
        # Fetch the category by ID from the database
        stmt = db.select(Category).filter_by(id=category_id)
        category = db.session.scalar(stmt)

        if not category:
            return {"error": f"Category with id {category_id} not found"}, 404

        db.session.delete(category)
        db.session.commit()
        return {"message": f"Category '{category.label}' deleted successfully"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while deleting the category"}, 500
    
# Edit an existing category - PATCH
@categories_bp.route("/<int:category_id>", methods=["PATCH", "PUT"])
@jwt_required()
def edit_category(category_id):
    """Edit an existing category by its ID.
    This endpoint allows an authenticated user to update a category.

    Args:
        category_id (int): The ID of the category to be updated.

    Request JSON Body:
        label (str): The new name of the category.

    Returns:
        JSON: The updated category data or an error message.
        200: Category updated successfully.
        400: Validation error in the request data.
        404: Category not found.
        500: Internal server error.
    """
    try:
        body_data = request.get_json()

        # Fetch the category by ID from the database
        stmt = db.select(Category).filter_by(id=category_id)
        category = db.session.scalar(stmt)

        if not category:
            return {"error": f"Category with id {category_id} not found"}, 404

        # Validate the unique label
        existing_category = Category.query.filter_by(label=body_data['label']).first()
        if existing_category and existing_category.id != category_id:
            return {"error": "A category with this label already exists."}, 400

        # Update the category label
        if 'label' in body_data:
            category.label = body_data['label']

        db.session.commit()

        return category_schema.dump(category), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while updating the category"}, 500

    except Exception:
        return {"error": "An unexpected error occurred while updating the category"}, 500















