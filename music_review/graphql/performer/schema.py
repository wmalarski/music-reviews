import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .filters import PerformerFilter
from .mutations import CreatePerformer, UpdatePerformer, DeletePerformer
from .types import PerformerType


class PerformerMutations(graphene.ObjectType):
    create_performer = CreatePerformer.Field()
    update_performer = UpdatePerformer.Field()
    delete_performer = DeletePerformer.Field()


class PerformerQuery(graphene.ObjectType):
    performer_set = DjangoFilterConnectionField(
        PerformerType, filterset_class=PerformerFilter
    )
    performer = graphene.relay.Node.Field(PerformerType)
