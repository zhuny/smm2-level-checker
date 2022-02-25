import base64
import random
from typing import Dict

import graphene
from flask_login import current_user
from graphene import relay, Scalar
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.language import ast
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import contains_eager, joinedload

from server.model import Team, Maker, Level, LevelDifficulty, LevelClear, db, TeamSearchOption
from server.schema_util import SQLAlchemyQueryField


class TeamSearchOptionSchema(SQLAlchemyObjectType):
    class Meta:
        model = TeamSearchOption
        interfaces = relay.Node,


class TeamSchema(SQLAlchemyObjectType):
    class Meta:
        model = Team
        interfaces = relay.Node,
        exclude_fields = "option_list",

    search_option = graphene.Field(TeamSearchOptionSchema)


class MakerSchema(SQLAlchemyObjectType):
    class Meta:
        model = Maker
        interfaces = relay.Node,


class LevelClearSchema(SQLAlchemyObjectType):
    class Meta:
        model = LevelClear
        interfaces = relay.Node,


class LevelSchema(SQLAlchemyObjectType):
    class Meta:
        model = Level
        interfaces = relay.Node,
        exclude_fields = "clear_list",

    clear_info = graphene.Field(LevelClearSchema)


class LevelDifficultySchema(SQLAlchemyObjectType):
    class Meta:
        model = LevelDifficulty
        interfaces = relay.Node,


class Base64Key(Scalar):
    def __init__(self, key_name: str):
        super().__init__()
        self.key_name = key_name

    def serialize(self, data):
        return base64.b64decode(f"{self.key_name}:{data}")

    @staticmethod
    def parse_value(data):
        name, key = base64.b64decode(data).decode().split(':', 1)
        if key.isdigit():
            return int(key)

    @classmethod
    def parse_literal(cls, data):
        if isinstance(data, ast.StringValue):
            return cls.parse_value(data.value)


class DifficultyRangeInput(graphene.InputObjectType):
    team_id = Base64Key("TeamSchema")
    range_start = graphene.Decimal()
    range_end = graphene.Decimal()


class RandomLevelSchema(graphene.Mutation):
    class Arguments:
        team_info_list = graphene.List(DifficultyRangeInput)

    Output = LevelSchema

    _valid_char = "0123456789ABCDEFGHJKLMNPQRSTUVWXY"

    @classmethod
    def _get_random_code(cls):
        return "-".join([
            "".join(random.choices(cls._valid_char, k=3))
            for _ in range(3)
        ])

    @classmethod
    def _save_team_info(cls, team_info_list):
        query = db.session.query(TeamSearchOption).filter(
            TeamSearchOption.user_id == current_user.user_id
        )
        option_map: Dict[int, TeamSearchOption] = {
            row.team_id: row
            for row in query
        }
        for row in option_map.values():
            row.selected = False
        for team_info in team_info_list:
            if team_info['team_id'] in option_map:
                row = option_map[team_info['team_id']]
            else:
                row = option_map[team_info['team_id']] = TeamSearchOption()
                row.user_id = current_user.user_id
                row.team_id = team_info['team_id']

            row.range_start = team_info['range_start']
            row.range_end = team_info['range_end']
            row.selected = True
        db.session.add_all(option_map.values())

    def mutate(self, info, team_info_list):
        # 조건에 맞는 맵을 쿼리한다.
        query = LevelDifficultySchema.get_query(
            info
        ).filter(or_(*[
            and_(
                LevelDifficulty.team_id == team_info['team_id'],
                LevelDifficulty.difficulty >= team_info['range_start'],
                LevelDifficulty.difficulty <= team_info['range_end']
            )
            for team_info in team_info_list
        ])).join(
            LevelDifficulty.level
        ).options(
            contains_eager(LevelDifficulty.level)
        ).order_by(
            Level.code
        )
        random_level = query.filter(
            Level.code >= RandomLevelSchema._get_random_code()
        ).first() or query.first()

        # 검색한 조건을 이후에 재사용하기 위해 저장한다.
        RandomLevelSchema._save_team_info(team_info_list)

        db.session.commit()

        if random_level:
            return random_level.level


class ClearLevelSchema(graphene.Mutation):
    class Arguments:
        level_id = Base64Key("LevelSchema")

    Output = LevelSchema

    def mutate(self, info, level_id):
        if current_user.is_anonymous:
            return

        level = LevelSchema.get_query(
            info
        ).filter(
            Level.id == level_id
        ).first()
        level.clear_list.append(
            LevelClear(
                user_id=current_user.user_id,
                clear_at=func.now()
            )
        )
        db.session.add(level)
        db.session.commit()
        return level


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_team = SQLAlchemyQueryField(TeamSchema)
    all_maker = SQLAlchemyQueryField(MakerSchema)
    all_level = SQLAlchemyQueryField(LevelSchema)

    team = relay.Node.Field(TeamSchema)
    maker = relay.Node.Field(MakerSchema)
    level = relay.Node.Field(LevelSchema)


class Mutation(graphene.ObjectType):
    random_level = RandomLevelSchema.Field()
    clear_level = ClearLevelSchema.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
