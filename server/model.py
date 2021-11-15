from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


def init(app: Flask):
    db.init_app(app)
