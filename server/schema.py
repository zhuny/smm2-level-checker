import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from server.model import TestModel


class TestSchema(SQLAlchemyObjectType):
    class Meta:
        model = TestModel
        interfaces = relay.Node,


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_tests = SQLAlchemyConnectionField(TestSchema.connection)


schema = graphene.Schema(query=Query)
