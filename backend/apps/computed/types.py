from email.policy import default
import graphene
from apps.flows.types import ChannelType


class ComputedGameDataType(graphene.ObjectType):
    data = graphene.List(
        graphene.Decimal, array=graphene.List(graphene.Decimal))
    channel = graphene.Field(ChannelType)
    is_total = graphene.Boolean()
    month_key = graphene.Int()