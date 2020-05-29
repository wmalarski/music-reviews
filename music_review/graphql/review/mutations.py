import graphene

from .types import ReviewType
from ...reviews.models import Review


class CreateReview(graphene.relay.ClientIDMutation):
    review = graphene.Field(ReviewType)

    class Input:
        album = graphene.ID(required=True)
        review = graphene.String(required=True)
        rating = graphene.Float(required=True)

    @classmethod
    def mutate_and_get_payload(cls, _, info, album: str, **kwargs):
        album = graphene.relay.Node.get_node_from_global_id(info, album)
        review = Review.objects.create(album=album, **kwargs,)
        return CreateReview(review=review)


class UpdateReview(graphene.relay.ClientIDMutation):
    review = graphene.Field(ReviewType)

    class Input:
        review_id = graphene.ID(required=True)
        album = graphene.ID()
        review = graphene.String()
        rating = graphene.Float()

    @classmethod
    def mutate_and_get_payload(cls, _, info, review_id: str, **kwargs):
        kwargs_cpy = kwargs.copy()
        review_instance = graphene.relay.Node.get_node_from_global_id(info, review_id)
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
    def mutate_and_get_payload(cls, _, info, review: str):
        review_instance = graphene.relay.Node.get_node_from_global_id(info, review)
        if review_instance is None:
            return DeleteReview(success=False)
        review_instance.delete()
        return DeleteReview(success=True)
