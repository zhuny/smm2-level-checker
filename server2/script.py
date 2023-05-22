import re

import click
import requests
from flask import current_app, Flask
from flask.cli import AppGroup
from tqdm import tqdm

from server2.model import Difficulty, Level, Team
from server2.storage import StorageController

app_group = AppGroup('smm2')


def load_team_info(team_slug):
    response = requests.post(
        "https://makerteams.net/backend/json",
        json={
            'url_slug': team_slug
        }
    )
    return response.json()


@app_group.command('view-level')
class ViewLevelCommand:
    def __init__(self):
        self.storage: StorageController = current_app.extensions['firestore']

        query = {
            'difficulty_list.difficulty': 2,
            'difficulty_list.team_slug': 'teamjamp'
        }
        for level in self.storage.get_list(Level, query=query):
            if len(level.difficulty_list) > 1:
                print(level)
                input()


@app_group.command('load-level')
class LoadLevelCommand:
    def __init__(self):
        self.storage: StorageController = current_app.extensions['firestore']
        for team in self.storage.get_list(Team):
            data = load_team_info(team.id)
            print(team.id)
            for level in tqdm(data['levels']):
                self.update_level_info(data['url_slug'], level)

    # 맵 정보 관련
    def update_level_info(self, team_slug, level_data):
        level = self.storage.get(Level, level_data['code'])
        if level is None:
            level = self.create_level_info(level_data)
        self.update_level_difficulty(level, level_data, team_slug)
        self.storage.save(level)

    def create_level_info(self, level_data):
        level_data = dict(level_data)
        level_data['id'] = level_data['code']
        level_tag = level_data.pop('tags')
        level: Level = Level.parse_obj(level_data)
        level.tags.update(level_tag.split(','))
        return level

    def update_level_difficulty(self,
                                level: Level, level_data: dict,
                                team_slug: str):
        for difficulty in level.difficulty_list:
            if difficulty.team_slug == team_slug:
                return

        level_data = dict(
            level_data,
            team_slug=team_slug
        )
        level.difficulty_list.append(
            Difficulty.parse_obj(level_data)
        )


@app_group.command('add-team')
@click.argument('team_slug')
class AddTeamCommand:
    def __init__(self, team_slug):
        self.storage: StorageController = current_app.extensions['firestore']
        data = load_team_info(team_slug)
        self.update_team_info(data)

    # 팀 정보 관련
    def update_team_info(self, data):
        """
        팀 정보 업데이트 하기
        """
        team = self.storage.get(Team, data['url_slug'])
        if team is None:
            team = self.create_team_info(data['url_slug'], data['teamSettings'])
            self.storage.save(team)
            print(team, 'added')
        else:
            print(team.id, 'exists')

    def create_team_info(self, team_slug, team_info):
        info = self.to_json_snake_case(team_info)
        info['id'] = team_slug
        return Team.parse_obj(info)

    def to_json_snake_case(self, obj: dict):
        return {
            self.to_snake_case(k): v
            for k, v in obj.items()
        }

    def to_snake_case(self, attr: str):
        attr = attr[0].upper() + attr[1:]
        return '_'.join([
            word.lower()
            for word in re.findall('[A-Z][a-z]*', attr)
        ])


def init(app: Flask):
    app.cli.add_command(app_group)
