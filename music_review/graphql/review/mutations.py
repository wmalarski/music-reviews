import graphene
from graphql_jwt.decorators import login_required

from .types import ReviewType
from ..utils import check_permissions
from ...reviews.models import Review


class CreateReview(graphene.relay.ClientIDMutation):
    review = graphene.Field(ReviewType)

    class Input:
        album = graphene.ID(required=True)
        review = graphene.String(required=True)
        rating = graphene.Float(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, album: str, **kwargs):
        album = graphene.relay.Node.get_node_from_global_id(info, album)
        review = Review.objects.create(album=album, user=info.context.user, **kwargs, )
        return CreateReview(review=review)


class UpdateReview(graphene.relay.ClientIDMutation):
    review = graphene.Field(ReviewType)

    class Input:
        review_id = graphene.ID(required=True)
        album = graphene.ID()
        review = graphene.String()
        rating = graphene.Float()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, review_id: str, **kwargs):
        kwargs_cpy = kwargs.copy()
        review_instance = graphene.relay.Node.get_node_from_global_id(info, review_id)
        check_permissions(review_instance.user, info)
        if album_id := kwargs_cpy.get("album"):
            kwargs_cpy["album"] = graphene.relay.Node.get_node_from_global_id(
                info, album_id
            )
        for key, value in kwargs_cpy.items():
            setattr(review_instance, key, value)
        review_instance.save()
        return UpdateReview(review=review_instance)


class DeleteReview(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()

    class Input:
        review = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, _, info, review: str):
        review_instance = graphene.relay.Node.get_node_from_global_id(info, review)
        check_permissions(review_instance.user, info)
        if review_instance is None:
            return DeleteReview(success=False)
        review_instance.delete()
        return DeleteReview(success=True)
