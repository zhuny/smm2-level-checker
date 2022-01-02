from flask import Flask
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, Integer, select
from sqlalchemy.ext.hybrid import hybrid_property


class ModelBase(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)


db = SQLAlchemy(model_class=ModelBase)


class Team(db.Model):
    team_name = db.Column(db.Text)
    discord_invite = db.Column(db.Text)
    twitter_user = db.Column(db.Text)
    primary_color = db.Column(db.Text)
    secondary_color = db.Column(db.Text)
    max_difficulty = db.Column(db.Integer)

    @property
    def search_option(self):
        # Query Optimization
        for option in self.option_list:
            if option.user_id == current_user.user_id:
                return option


class TeamSearchOption(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    team = db.relationship("Team", backref=db.backref("option_list"))
    user_id = db.Column(db.Integer, index=True)

    selected = db.Column(db.Boolean)
    range_start = db.Column(db.DECIMAL)
    range_end = db.Column(db.DECIMAL)


class Maker(db.Model):
    code = db.Column(db.Text)
    name = db.Column(db.Text)
    creator_id = db.Column(db.Integer)


class Level(db.Model):
    code = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey("maker.id"))
    creator = db.relationship("Maker")
    name = db.Column(db.Text)

    @hybrid_property
    def clear_info(self):
        for clear in self.clear_list:
            return clear

    @clear_info.expression
    def clear_info(cls):
        return select(
            LevelClear
        ).where(
            cls.id == LevelClear.level_id,
            LevelClear.user_id == current_user.user_id
        ).first()


class LevelClear(db.Model):
    level_id = db.Column(db.Integer, db.ForeignKey("level.id"))
    level = db.relationship("Level", backref=db.backref("clear_list"))
    user_id = db.Column(db.Integer, index=True)
    clear_at = db.Column(db.DateTime)


class LevelDifficulty(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    team = db.relationship("Team", backref=db.backref('level_list'))
    level_id = db.Column(db.Integer, db.ForeignKey("level.id"))
    level = db.relationship("Level", backref=db.backref('difficulty_list'))

    difficulty = db.Column(db.DECIMAL)
    clears = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    tags = db.Column(db.Text)

    submission_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)


def init(app: Flask):
    db.init_app(app)
