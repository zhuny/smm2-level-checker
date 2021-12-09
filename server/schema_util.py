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
            issubclass(schema.graphene_type, SQLAlchemyObjectType)
        )

    @classmethod
    def _build_query_join_schema(cls, model, query, parent_type, asts):
        for f in asts:
            this_schema = cls._get_schema(parent_type, f.name.value)
            this_type = this_schema.type
            if cls._is_sql_schema(parent_type) and cls._is_sql_schema(this_type):
                # TODO: auto_camel_case = False 인 경우 구분해주기
                # TODO: nested한 경우도 처리해주기
                snake_name = to_snake_case(f.name.value)
                query = query.options(
                    joinedload(getattr(model, snake_name))
                )
            if f.selection_set:
                query = cls._build_query_join_schema(
                    model,
                    query,
                    this_type,
                    f.selection_set.selections
                )
        return query

    @classmethod
    def get_query(cls, model, info: ResolveInfo = None, sort=None, **args):
        query = super().get_query(model, info, sort=sort, **args)
        root_type = info.schema.get_query_type()
        return cls._build_query_join_schema(
            model, query, root_type, info.field_asts
        )
