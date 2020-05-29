import graphene as graphene
from graphene_django.filter import DjangoFilterConnectionField

from .types import UserType


class UserQuery(graphene.ObjectType):
    user_set = DjangoFilterConnectionField(UserType, fields=["username"])
