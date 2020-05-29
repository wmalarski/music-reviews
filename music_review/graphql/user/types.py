from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (relay.Node,)
        exclude = ("password",)
