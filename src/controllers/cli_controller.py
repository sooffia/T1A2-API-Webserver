from datetime import date, datetime
from flask import Blueprint
from init import db, bcrypt
from models.users import User
from models.task import Task
from models.comment import Comment
from models.category import Category 

db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def create_tables():
    """Creates the database tables."""
    db.create_all()
    print("Database tables created")

@db_commands.cli.command("drop")
def drop_tables():
    """Drops the database tables."""
    db.drop_all()
    print("Database tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    """Seeds the database tables.

    Table values are specified and committed in the following order due to relationships:
        Users
        Category 
        Tasks
        Comments
    """
    users = [
        User(
            name="Admin User",
            email="admin@domain.com",
            password=bcrypt.generate_password_hash("securepassword").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="Alice Johnson",
            email="alice.johnson@example.com",
            password=bcrypt.generate_password_hash("alice1234").decode("utf-8"),
        ),
        User(
            name="Bob Smith",
            email="bob.smith@example.com",
            password=bcrypt.generate_password_hash("bobpassword").decode("utf-8"),
        ),
        User(
            name="Charlie Brown",
            email="charlie.brown@example.com",
            password=bcrypt.generate_password_hash("charliepass").decode("utf-8"),
        )
    ]
    
    db.session.add_all(users)
    db.session.commit()
    
    categories = [
        Category(label="Work"),
        Category(label="Personal"),
        Category(label="Team Collaboration"),
        Category(label="On Hold")
    ]

    db.session.add_all(categories)
    db.session.commit()

    tasks = [
        Task(
            title="Complete Project Report",
            description="Prepare and submit the final project report by the end of the week.",
            due_date=date.today(),
            status="To Do",
            user=users[0], 
            category=categories[1]
            ),

        Task(
            title="Develop New Feature",
            description="Work on developing the new authentication feature for the app.",
            due_date=date.today(),
            status="In Progress",
            user=users[1], 
            category=categories[2]
            ),

        Task(
            title="Update Documentation",
            description="Update the API documentation to reflect recent changes.",
            due_date=date.today(),
            status="Completed",
            user=users[2],
            category=categories[3]
        ),

        Task(
            title="Fix Bugs",
            description="Identify and fix bugs reported in the latest release.",
            due_date=date.today(),
            status="To Do",
            user=users[3], 
            category=categories[2]
            )
    ]
    
    db.session.add_all(tasks)
    db.session.commit()

    comments = [
        Comment(
            content="Make sure to include the financial summary in the report.",
            timestamp=datetime.now(),
            task=tasks[0],
            user=users[1]
            ),

        Comment(
            content="The new feature looks good, but needs more testing.",
            timestamp=datetime.now(),
            task=tasks[1],
            user=users[2]
            ),

        Comment(
            content="Documentation is up to date with the latest changes.",
            timestamp=datetime.now(),
            task=tasks[2],
            user=users[3]
            ),

        Comment(
            content="Found a critical bug in the login module.",
            timestamp=datetime.now(),
            task=tasks[3],
            user=users[0]
            )
        ]

    db.session.add_all(comments)
    db.session.commit()

    print("Database tables seeded")