from datetime import date, datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity 
from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.task import Task 


comments_bp = Blueprint("comments", __name__,url_prefix="/<int:task_id>/comments")

# we already recieve the comments while fetching tasks, so no need to put the comments route here 
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(task_id):
    body_data = request.get_json()
    stmt = db.select(Task).filter_by(id=task_id)
    task = db.session.scalar(stmt)
    if task:
        comment = Comment(
            content=body_data.get("content"), 
            timestamp=datetime.now(),
            task=task, 
            user_id=get_jwt_identity()
        )

        db.session.add(comment)
        db.session.commit()

        return comment_schema.dump(comment), 201
    else:
        return {"error":f"Task with id {task_id} not found"}, 404

#delete comment 
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(task_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        db.session.delete(comment)
        db.session.commit()

        return {"message": f"Comment: {comment.content} has been deleted successfully"}
    else:
        return {"error": f"Comment with id {comment_id} not found"}, 404 
    

    













    



