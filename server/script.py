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


def from_string(string):
    return datetime.datetime.fromisoformat(string.strip('Z'))


@app_group.command('load')
@click.argument('data_file')
def load_data(data_file):
    with open(data_file, encoding="utf8") as f:
        data = json.load(f)

        # save team table
        team_setting = data['teamSettings']
        team_row = db.session.query(
            Team
        ).filter(
            Team.team_name == team_setting['TeamName']
        ).first() or Team()
        team_row.team_name = team_setting['TeamName']
        team_row.discord_invite = team_setting['DiscordInvite']
        team_row.twitter_user = team_setting['TwitterUser']
        team_row.primary_color = team_setting['PrimaryColor']
        team_row.secondary_color = team_setting['SecondaryColor']
        team_row.max_difficulty = team_setting['maxDifficulty']
        db.session.add(team_row)

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
        difficulty_map = collections.defaultdict(LevelDifficulty, {
            difficulty.level.code: difficulty
            for difficulty in db.session.query(LevelDifficulty)
        })
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
