import base64
import random

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import joinedload

from server.model import Team, Maker, Level, LevelDifficulty, db


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


def _convert(team_id):
    decoded_id = base64.b64decode(team_id).decode()
    schema_name, row_id = decoded_id.split(':')
    return int(row_id)


class RandomLevelSchema(graphene.Mutation):
    class Arguments:
        team_id = relay.node.ID()
        range_start = graphene.Decimal()
        range_end = graphene.Decimal()

    Output = LevelSchema

    def mutate(self, info, team_id, range_start, range_end):
        random_levels = LevelDifficultySchema.get_query(info).filter(
            LevelDifficulty.team_id == _convert(team_id),
            LevelDifficulty.difficulty >= range_start,
            LevelDifficulty.difficulty <= range_end
        ).options(
            joinedload(LevelDifficulty.level)
        ).limit(10).all()  # 적당히 랜덤하게 쿼리 작성할 수 있도록 수정
        return random.choice(random_levels).level


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_team = SQLAlchemyConnectionField(TeamSchema.connection)
    all_maker = SQLAlchemyConnectionField(MakerSchema.connection)
    all_level = SQLAlchemyConnectionField(LevelSchema.connection)


class Mutation(graphene.ObjectType):
    random_level = RandomLevelSchema.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
