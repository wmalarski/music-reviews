import graphene

from .types import AlbumType
from ...reviews.models import Album


class CreateAlbum(graphene.relay.ClientIDMutation):
    album = graphene.Field(AlbumType)

    class Input:
        performer = graphene.ID(required=True)
        title = graphene.String(required=True)
        year = graphene.Int(required=True)
        cover_url = graphene.String()
        description = graphene.String(default="")

    @classmethod
    def mutate_and_get_payload(cls, _, info, performer: str, **kwargs):
        performer = graphene.relay.Node.get_node_from_global_id(info, performer)
        album = Album.objects.create(performer=performer, **kwargs,)
        return CreateAlbum(album=album)


class UpdateAlbum(graphene.relay.ClientIDMutation):
    album = graphene.Field(AlbumType)

    class Input:
        album = graphene.ID(required=True)
        performer = graphene.ID()
        title = graphene.String()
        year = graphene.Int()
        cover_url = graphene.String()
        description = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, _, info, album: str, **kwargs):
        kwargs_cpy = kwargs.copy()
        album_instance = graphene.relay.Node.get_node_from_global_id(info, album)
        if performer_id := kwargs_cpy.get("performer"):
            kwargs_cpy["performer"] = graphene.relay.Node.get_node_from_global_id(
                info, performer_id
            )
        for key, value in kwargs_cpy.items():
            setattr(album_instance, key, value)
        album_instance.save()
        return UpdateAlbum(album=album_instance)


class DeleteAlbum(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()

    class Input:
        album = graphene.ID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, _, info, album: str):
        album_instance = graphene.relay.Node.get_node_from_global_id(info, album)
        if album_instance is None:
            return DeleteAlbum(success=False)
        album_instance.delete()
        return DeleteAlbum(success=True)
