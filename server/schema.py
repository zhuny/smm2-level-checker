import base64
import random

import graphene
from graphene import relay, Scalar
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql.language import ast
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

from server.model import Team, Maker, Level, LevelDifficulty


class TeamSchema(SQLAlchemyObjectType):
    class Meta:
        model = Team
        interfaces = relay.Node,


class MakerSchema(SQLAlchemyObjectType):
    class Meta:
        model = Maker
        interfaces = relay.Node,


class LevelSchema(SQLAlchemyObjectType):
    class Meta:
        model = Level
        interfaces = relay.Node,


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

    def mutate(self, info, team_info_list):
        random_levels = LevelDifficultySchema.get_query(
            info
        ).filter(or_(*[
            and_(
                LevelDifficulty.team_id == team_info['team_id'],
                LevelDifficulty.difficulty >= team_info['range_start'],
                LevelDifficulty.difficulty <= team_info['range_end']
            )
            for team_info in team_info_list
        ])).options(
            joinedload(LevelDifficulty.level)
        ).limit(10).all()  # 적당히 랜덤하게 쿼리 작성할 수 있도록 수정
        if random_levels:
            return random.choice(random_levels).level


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_team = SQLAlchemyConnectionField(TeamSchema.connection)
    all_maker = SQLAlchemyConnectionField(MakerSchema.connection)
    all_level = SQLAlchemyConnectionField(LevelSchema.connection)


class Mutation(graphene.ObjectType):
    random_level = RandomLevelSchema.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
