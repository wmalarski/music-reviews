from typing import Optional, List, Dict

import graphene
from graphql_jwt.decorators import login_required

from .types import PerformerType
from ..utils import check_permissions
from ...reviews.models import Performer, Album


class AlbumInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    year = graphene.Int(required=True)
    cover_url = graphene.String()
    description = graphene.String()


class CreatePerformer(graphene.relay.ClientIDMutation):
    performer = graphene.Field(PerformerType)

    class Input:
        name = graphene.String(required=True)
        logo_url = graphene.String()
        description = graphene.String(default="")
        albums = graphene.List(graphene.NonNull(AlbumInputType), default=[])

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        _,
        info,
        name: str,
        logo_url: Optional[str] = None,
        description: Optional[str] = "",
        albums: List[AlbumInputType] = (),
    ):
        performer = Performer.objects.create(
            name=name, logo_url=logo_url, description=description, user=info.context.user
        )
        for album in albums:
            Album.objects.create(
                performer=performer,
                title=album.title,
                year=album.year,
                cover_url=album.cover_url,
                description=album.description,
                user=info.context.user,
            )

        return CreatePerformer(performer=performer)


class UpdatePerformer(graphene.relay.ClientIDMutation):
    performer = graphene.Field(PerformerType)

    class Input:
        performer = graphene.ID(required=True)
        name = graphene.String()
        logo_url = graphene.String()
        description = graphene.String()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, performer: str, **kwargs: Dict[str, str]):
        performer_instance = graphene.relay.Node.get_node_from_global_id(
            info, performer
        )
        check_permissions(performer_instance.user, info)
        for key, value in kwargs.items():
            setattr(performer_instance, key, value)
        performer_instance.save()
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
