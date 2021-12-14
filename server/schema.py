import base64
import random

import graphene
from graphene import relay, Scalar
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.language import ast
from sqlalchemy import or_, and_
from sqlalchemy.orm import contains_eager

from server.model import Team, Maker, Level, LevelDifficulty, LevelClear
from server.schema_util import SQLAlchemyQueryField


class TeamSchema(SQLAlchemyObjectType):
    class Meta:
        model = Team
        interfaces = relay.Node,


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

    def mutate(self, info, team_info_list):
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
        if random_level:
            return random_level.level


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_team = SQLAlchemyQueryField(TeamSchema)
    all_maker = SQLAlchemyQueryField(MakerSchema)
    all_level = SQLAlchemyQueryField(LevelSchema)

    level = relay.Node.Field(LevelSchema)


class Mutation(graphene.ObjectType):
    random_level = RandomLevelSchema.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
