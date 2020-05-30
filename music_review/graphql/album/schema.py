import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .filters import AlbumFilter
from .mutations import CreateAlbum, UpdateAlbum, DeleteAlbum
from .types import AlbumType


class AlbumMutations(graphene.ObjectType):
    create_album = CreateAlbum.Field()
    update_album = UpdateAlbum.Field()
    delete_album = DeleteAlbum.Field()


class AlbumQuery(graphene.ObjectType):
    album_set = DjangoFilterConnectionField(AlbumType, filterset_class=AlbumFilter)
    album = graphene.relay.Node.Field(AlbumType)
