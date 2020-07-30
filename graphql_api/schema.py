import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphql_api.users.schema import Mutation as user_mutation, Query as user_query

class Query(user_query, graphene.ObjectType):
    pass


class Mutation(user_mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
