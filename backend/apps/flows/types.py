from apps.flows.models import Flow, Card, Channel, StageInSequence, Stage, ParameterChange, StageOfChannel
from graphene_django.types import DjangoObjectType


class FlowType(DjangoObjectType):
    class Meta:
        model = Flow
        fields = "__all__"


class CardType(DjangoObjectType):
    class Meta:
        model = Card
        fields = "__all__"


class ChannelType(DjangoObjectType):
    class Meta:
        model = Channel
        fields = "__all__"


class StageInSequenceType(DjangoObjectType):
    class Meta:
        model = StageInSequence
        fields = "__all__"


class StageType(DjangoObjectType):
    class Meta:
        model = Stage
        fields = "__all__"

class StageOfChannelType(DjangoObjectType):
    class Meta:
        model = StageOfChannel
        fields = "__all__"


# class ParameterChangeType(DjangoObjectType):
#     class Meta:
#         model = ParameterChange
#         fields = "__all__"
