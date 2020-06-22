from typing import Dict, Any

import graphene
from graphql_jwt.decorators import login_required

from .types import AlbumType
from ..utils import check_permissions, update_and_save
from ...reviews.models import Album


class CreateAlbum(graphene.relay.ClientIDMutation):
    album = graphene.Field(AlbumType)

    class Input:
        performer = graphene.ID(required=True)
        mbid = graphene.String(required=True)
        name = graphene.String(required=True)
        year = graphene.Int(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, performer: str, **kwargs: Dict[str, Any]):
        performer = graphene.relay.Node.get_node_from_global_id(info, performer)
        album = Album.objects.create(
            performer=performer, user=info.context.user, **kwargs
        )
        return CreateAlbum(album=album)


class UpdateAlbum(graphene.relay.ClientIDMutation):
    album = graphene.Field(AlbumType)

    class Input:
        album = graphene.ID(required=True)
        mbid = graphene.String()
        name = graphene.String()
        year = graphene.Int()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, album: str, **kwargs: Dict[str, Any]):
        album_instance = graphene.relay.Node.get_node_from_global_id(info, album)
        check_permissions(album_instance.user, info)
        update_and_save(album_instance, kwargs)
        return UpdateAlbum(album=album_instance)


class DeleteAlbum(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()

    class Input:
        album = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, album: str):
        album_instance = graphene.relay.Node.get_node_from_global_id(info, album)
        check_permissions(album_instance.user, info)
        if album_instance is None:
            return DeleteAlbum(success=False)
        album_instance.delete()
        return DeleteAlbum(success=True)
