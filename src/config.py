from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

import os

app = Flask("app")
db = SQLAlchemy(app)
marsh = Marshmallow(app)
jwt = JWTManager(app)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "resume.db"
)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
