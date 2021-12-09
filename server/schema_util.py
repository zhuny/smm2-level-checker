from graphene.relay.connection import Connection
from graphene.types.definitions import GrapheneObjectType
from graphene.utils.str_converters import to_snake_case
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql import GraphQLNonNull, GraphQLList, ResolveInfo
from sqlalchemy.orm import joinedload


class SQLAlchemyQueryField(SQLAlchemyConnectionField):
    def __init__(self, schema):
        self.schema_name = type(schema).__name__
        super().__init__(schema.connection)

    @classmethod
    def _get_schema(cls, schema, name):
        schema = cls._get_primary_type(schema)
        return schema.fields[name]

    @classmethod
    def _get_primary_type(cls, schema):
        while isinstance(schema, (GraphQLNonNull, GraphQLList)):
            schema = schema.of_type
        return schema

    @classmethod
    def _is_sql_schema(cls, schema):
        return (
            isinstance(schema, GrapheneObjectType) and
            (
                issubclass(schema.graphene_type, SQLAlchemyObjectType) or
                issubclass(schema.graphene_type, Connection)
            )
        )

    @classmethod
    def _get_sql_model(cls, t):
        return t.graphene_type._meta.model

    @classmethod
    def _build_query_join_schema(cls,
                                 model, parent_type, asts,
                                 joined=None,
                                 follow_backref=False):
        for f in asts:
            this_schema = cls._get_schema(parent_type, f.name.value)
            this_type = this_schema.type
            nested_follow = follow_backref
            if cls._is_sql_schema(parent_type) and cls._is_sql_schema(this_type):
                # backref로 생성된 경우,
                # connection-node를 거치고 나서 model정보를 알 수 있다
                if follow_backref:
                    model = cls._get_sql_model(parent_type)

                # TODO: auto_camel_case = False 인 경우 구분해주기
                snake_name = to_snake_case(f.name.value)

                # column join하기
                column = getattr(model, snake_name)
                if joined:
                    joined = joined.joinedload(column)
                else:
                    joined = joinedload(column)

                # nested를 위해 map column을 가져온다
                if issubclass(this_type.graphene_type, Connection):
                    nested_follow = True
                else:
                    model = cls._get_sql_model(this_type)

            # recursively 확인
            if f.selection_set:
                yield from cls._build_query_join_schema(
                    model,
                    this_type,
                    f.selection_set.selections,
                    joined,
                    nested_follow
                )
            elif joined:
                yield joined

    @classmethod
    def get_query(cls, model, info: ResolveInfo = None, sort=None, **args):
        query = super().get_query(model, info, sort=sort, **args)
        return query.options(
            *cls._build_query_join_schema(
                model,
                info.schema.get_query_type(),
                info.field_asts
            )
        )
