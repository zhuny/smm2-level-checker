import collections
import datetime
import json

import click
from flask import Flask
from flask.cli import AppGroup

from server.model import db, Team, Maker, Level, LevelDifficulty

app_group = AppGroup('init')


@app_group.command('table')
def init_create():
    db.create_all()
    # LevelClear.__table__.create(db.session.bind)


def from_string(string):
    return datetime.datetime.fromisoformat(string.strip('Z'))


class DataController:
    @classmethod
    def upsert_team(cls,
                    team_name,
                    discord_invite=None, twitter_user=None,
                    primary_color=None, secondary_color=None,
                    max_difficulty=None) -> Team:
        team_row = db.session.query(
            Team
        ).filter(
            Team.team_name == team_name
        ).first() or Team(team_name=team_name)

        team_row.discord_invite = discord_invite
        team_row.twitter_user = twitter_user
        team_row.primary_color = primary_color
        team_row.secondary_color = secondary_color
        team_row.max_difficulty = max_difficulty

        db.session.add(team_row)
        return team_row


@app_group.command('load-team')
@click.argument('data_file')
def load_team_data(data_file):
    with open(data_file, encoding="utf8") as f:
        data = json.load(f)

        # save team table
        team_setting = data['teamSettings']
        team_row = DataController.upsert_team(
            team_setting['TeamName'],
            discord_invite=team_setting['DiscordInvite'],
            twitter_user=team_setting['TwitterUser'],
            primary_color=team_setting['PrimaryColor'],
            secondary_color=team_setting['SecondaryColor'],
            max_difficulty=team_setting['maxDifficulty']
        )

        # setting maker first
        maker_map = collections.defaultdict(Maker, {
            maker.creator_id: maker
            for maker in db.session.query(Maker)
        })
        for level in data['levels']:
            maker_row = maker_map[level['creator_id']]
            maker_row.creator_id = level['creator_id']
            maker_row.code = level['maker_id']
            maker_row.name = level['creator']
            db.session.add(maker_row)

        # setting level
        level_map = collections.defaultdict(Level, {
            level.code: level
            for level in db.session.query(Level)
        })
        for level in data['levels']:
            level_row = level_map[level['code']]
            level_row.code = level['code']
            level_row.name = level['level_name']
            level_row.creator = maker_map[level['creator_id']]
            db.session.add(level_row)

        # saving difficulty
        difficulty_map = collections.defaultdict(LevelDifficulty)
        if team_row.id is not None:
            query = db.session.query(LevelDifficulty).filter(
                LevelDifficulty.level_id == team_row.id
            )
            for difficulty in query:
                difficulty_map[difficulty.level.code] = difficulty

        for level in data['levels']:
            difficulty_row = difficulty_map[level['code']]
            difficulty_row.team = team_row
            difficulty_row.level = level_map[level['code']]
            difficulty_row.difficulty = level['difficulty']
            difficulty_row.clears = level['clears']
            difficulty_row.likes = level['likes']
            difficulty_row.tags = level['tags']
            difficulty_row.submission_date = from_string(
                level['original_submission_date']
            )
            difficulty_row.created_at = from_string(level['created_at'])
            db.session.add(difficulty_row)

    db.session.commit()


def init(app: Flask):
    app.cli.add_command(app_group)
