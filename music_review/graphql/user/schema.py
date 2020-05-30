import graphene
import graphql_jwt

from graphene_django.filter import DjangoFilterConnectionField

from .types import UserType


class UserQuery(graphene.ObjectType):
    user_set = DjangoFilterConnectionField(UserType, fields=["username"])
    user = graphene.relay.Node.Field(UserType)


class UserMutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
