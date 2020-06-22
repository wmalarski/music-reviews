from graphene import relay
from graphene_django import DjangoObjectType
from graphene_federation import key

from ...reviews.models import Performer


@key("mbid")
class PerformerType(DjangoObjectType):
    class Meta:
        model = Performer
        interfaces = (relay.Node,)
