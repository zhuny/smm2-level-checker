import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

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


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_team = SQLAlchemyConnectionField(TeamSchema.connection)
    all_maker = SQLAlchemyConnectionField(MakerSchema.connection)
    all_level = SQLAlchemyConnectionField(LevelSchema.connection)


schema = graphene.Schema(query=Query)
