import graphene
from graphene_django.debug import DjangoDebug
from apps.flows.types import ChannelType, StageType
from apps.flows.types import CardType
from apps.flows.models import Channel, Stage, Card, Flow
from apps.organizations.models import Organization
from apps.rooms.models import Room


class Query(graphene.ObjectType):
    debug_flows = graphene.Field(DjangoDebug, name='__debug_flows')
    channels_by_code = graphene.List(
        ChannelType, description='Каналы игровой таблицы по коду комнаты', code=graphene.String())
    stages_by_code = graphene.List(
        StageType, description="Этапы игровой таблицы по коду комнаты", code=graphene.String())
    cards_by_code = graphene.List(CardType, code=graphene.String())

    def resolve_cards_by_code(root, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                flow = Flow.objects.get(pk=room.flow.id)
                return Card.objects.filter(flow=flow)
        except Exception as e:
            return None

    def resolve_channels_by_code(root, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
            return Channel.objects.filter(flow=room.flow)
        except Exception as e:
            return None

    def resolve_stages_by_code(root, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
            return Stage.objects.filter(flow=room.flow)
        except Exception as e:
            return None


class Mutation(graphene.ObjectType):
    pass
