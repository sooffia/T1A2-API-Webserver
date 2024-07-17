# connect intialised modules/libraies to the flask application 
from flask import Flask 
from init import db, ma, bcrypt, jwt 

#application factories 
def create_app(): 
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"