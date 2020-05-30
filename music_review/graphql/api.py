import graphene
from graphene_federation import build_schema

from music_review.graphql.album.schema import AlbumQuery, AlbumMutations
from music_review.graphql.performer.schema import PerformerQuery, PerformerMutations
from music_review.graphql.review.schema import ReviewQuery, ReviewMutations
from music_review.graphql.user.schema import UserQuery, UserMutations


class Query(AlbumQuery, PerformerQuery, ReviewQuery, UserQuery, graphene.ObjectType):
    pass


class Mutation(
    AlbumMutations, PerformerMutations, ReviewMutations, UserMutations, graphene.ObjectType
):
    pass


schema = build_schema(query=Query, mutation=Mutation)
