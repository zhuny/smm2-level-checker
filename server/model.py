from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


def init(app: Flask):
    db.init_app(app)
