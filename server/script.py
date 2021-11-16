from flask import Flask
from flask.cli import AppGroup

from server.model import db

app_group = AppGroup('init')


@app_group.command('table')
def init_create():
    db.create_all()


def init(app: Flask):
    app.cli.add_command(app_group)
