import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .filters import ReviewFilter
from .mutations import CreateReview, UpdateReview, DeleteReview
from .types import ReviewType


class ReviewMutations(graphene.ObjectType):
    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
    delete_review = DeleteReview.Field()


class ReviewQuery(graphene.ObjectType):
    review_set = DjangoFilterConnectionField(ReviewType, filterset_class=ReviewFilter)
    review = graphene.relay.Node.Field(ReviewType)
