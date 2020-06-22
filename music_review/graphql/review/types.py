from graphene import relay
from graphene_django import DjangoObjectType
from graphene_federation import key

from ...reviews.models import Review


@key("mbid")
class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        interfaces = (relay.Node,)
