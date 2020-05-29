from graphene import relay
from graphene_django import DjangoObjectType

from ...reviews.models import Performer


class PerformerType(DjangoObjectType):
    class Meta:
        model = Performer
        interfaces = (relay.Node,)
