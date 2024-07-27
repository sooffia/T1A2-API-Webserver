from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.task import Task
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

comments_bp = Blueprint("comments", __name__, url_prefix="/<int:task_id>/comments")

# Endpoint to create a new comment for a task
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(task_id):
    """Creates a new comment for a specific task.
    This endpoint allows an authenticated user to add a comment to a task.

    Args:
        task_id (int): The ID of the task to which the comment will be added.

    Request JSON Body:
        content (str): The content of the comment.

    Returns:
        JSON: The created comment's data or an error message.
        201: Comment created successfully.
        400: Validation error in the request data.
        404: Task not found.
        500: Internal server error.
    """
    try:
        # Get the request body data**
        body_data = request.get_json()
        
        # Validate the request data
        try:
            comment_data = comment_schema.load(body_data, partial=True)
        except ValidationError as err:
            return {"error": "Invalid data", "messages": err.messages}, 400

        # Fetch the task by ID from the database
        stmt = db.select(Task).filter_by(id=task_id)
        task = db.session.scalar(stmt)

        if not task:
            return {"error": f"Task with ID {task_id} not found"}, 404

        comment = Comment(
            content=comment_data.get("content"),
            timestamp=datetime.now(),
            task=task,
            user_id=get_jwt_identity()
        )
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while creating the comment"}, 500

# Endpoint to delete a comment by ID
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(task_id, comment_id):
    """Deletes a comment by its ID.
    This endpoint allows an authenticated user to delete a comment from a task.

    Args:
        task_id (int): The ID of the task from which the comment will be deleted.
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        JSON: Success message or error message.
        200: Comment deleted successfully.
        404: Task or comment not found.
        500: Internal server error.
    """
    try:
        # Fetch the task by ID from the database
        stmt = db.select(Task).filter_by(id=task_id)
        task = db.session.scalar(stmt)

        if not task:
            return {"error": f"Task with ID {task_id} not found"}, 404

        # Fetch the comment by ID from the database
        stmt = db.select(Comment).filter_by(id=comment_id)
        comment = db.session.scalar(stmt)

        if not comment:
            return {"error": f"Comment with ID {comment_id} not found"}, 404

        db.session.delete(comment)
        db.session.commit()
        return {"message": f"Comment '{comment.content}' has been deleted successfully"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while deleting the comment"}, 500

# Endpoint to update a comment by ID
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_comment(task_id, comment_id):
    """Updates a comment by its ID.
    This endpoint allows an authenticated user to update the content of a comment.

    Args:
        task_id (int): The ID of the task to which the comment belongs.
        comment_id (int): The ID of the comment to be updated.

    Request JSON Body:
        content (str): The new content of the comment.

    Returns:
        JSON: The updated comment's data or an error message.
        200: Comment updated successfully.
        400: Validation error in the request data.
        404: Task or comment not found.
        500: Internal server error.
    """
    try:
        body_data = request.get_json()

        # Validate the request data
        try:
            comment_data = comment_schema.load(body_data, partial=True)
        except ValidationError as err:
            return {"error": "Invalid data", "messages": err.messages}, 400

        # Fetch the task by ID from the database
        stmt = db.select(Task).filter_by(id=task_id)
        task = db.session.scalar(stmt)

        if not task:
            return {"error": f"Task with ID {task_id} not found"}, 404

        # Fetch the comment by ID from the database
        stmt = db.select(Comment).filter_by(id=comment_id)
        comment = db.session.scalar(stmt)

        if not comment:
            return {"error": f"Comment with ID {comment_id} not found"}, 404

        comment.content = comment_data.get("content", comment.content)
        db.session.commit()
        return comment_schema.dump(comment), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "An error occurred while updating the comment"}, 500
















    



