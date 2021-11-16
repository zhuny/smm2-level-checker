import collections
import json

import click
from flask import Flask
from flask.cli import AppGroup

from server.model import db, Team, Maker

app_group = AppGroup('init')


@app_group.command('table')
def init_create():
    db.create_all()


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
            maker.code: maker
            for maker in db.session.query(Maker)
        })
        for level in data['levels']:
            maker_row = maker_map[level['maker_id']]
            maker_row.code = level['maker_id']
            maker_row.name = level['creator']
            db.session.add(maker_row)

    db.session.commit()


def init(app: Flask):
    app.cli.add_command(app_group)
