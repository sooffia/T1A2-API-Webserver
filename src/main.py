# connect intialised modules/libraies to the flask application 
import os 
from flask import Flask 
from init import db, ma, bcrypt, jwt 


def create_app(): 
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.task_controller import tasks_bp
    app.register_blueprint(tasks_bp)

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
