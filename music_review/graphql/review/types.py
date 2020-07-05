from graphene import relay
from graphene_django import DjangoObjectType

from ...reviews.models import Review


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        interfaces = (relay.Node,)
