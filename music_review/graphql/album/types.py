from graphene import relay
from graphene_django import DjangoObjectType
from graphene_federation import key

from ...reviews.models import Album


@key("mbid")
class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        interfaces = (relay.Node,)
