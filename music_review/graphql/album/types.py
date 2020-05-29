from graphene import relay
from graphene_django import DjangoObjectType

from ...reviews.models import Album


class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        interfaces = (relay.Node,)
