from typing import Optional, List, Dict

import graphene
from graphql_jwt.decorators import login_required

from .types import PerformerType
from ..utils import check_permissions, update_and_save
from ...reviews.models import Performer, Album


class AlbumInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
    year = graphene.Int(required=True)
    mbid = graphene.String(required=True)


class CreatePerformer(graphene.relay.ClientIDMutation):
    performer = graphene.Field(PerformerType)

    class Input:
        mbid = graphene.String(required=True)
        name = graphene.String(required=True)
        albums = graphene.List(graphene.NonNull(AlbumInputType), default=[])

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        _,
        info,
        mbid: str,
        name: str,
        albums: Optional[List[AlbumInputType]] = None,
    ):
        albums = albums or []
        performer = Performer.objects.create(
            mbid=mbid, name=name, user=info.context.user,
        )
        for album in albums:
            Album.objects.create(
                performer=performer,
                name=album.name,
                mbid=album.mbid,
                year=album.year,
                user=info.context.user,
            )
        return CreatePerformer(performer=performer)


class UpdatePerformer(graphene.relay.ClientIDMutation):
    performer = graphene.Field(PerformerType)

    class Input:
        performer = graphene.ID(required=True)
        mbid = graphene.String()
        name = graphene.String()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, performer: str, **kwargs: Dict[str, str]):
        performer_instance = graphene.relay.Node.get_node_from_global_id(
            info, performer
        )
        check_permissions(performer_instance.user, info)
        update_and_save(performer_instance, kwargs)
        return UpdatePerformer(performer=performer_instance)


class DeletePerformer(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()

    class Input:
        performer = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, performer: str):
        performer_instance = graphene.relay.Node.get_node_from_global_id(
            info, performer
        )
        check_permissions(performer_instance.user, info)
        if performer_instance is None:
            return DeletePerformer(success=False)
        performer_instance.delete()
        return DeletePerformer(success=True)
