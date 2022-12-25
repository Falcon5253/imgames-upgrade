import graphene
from apps.rooms.models import CardChoice, Winner, Turn, Month, Round, Room, RoomParticipant, Message, Queue
from apps.organizations.models import Organization
from graphene_django.types import DjangoObjectType


class RoomParticipantType(DjangoObjectType):
    class Meta:
        model = RoomParticipant
        fields = "__all__"


class CardChoiceType(DjangoObjectType):
    class Meta:
        model = CardChoice
        fields = "__all__"


class WinnerType(DjangoObjectType):
    class Meta:
        model = Winner
        fields = "__all__"

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = "__all__"

class TurnType(DjangoObjectType):
    class Meta:
        model = Turn
        fields = "__all__"


class MonthType(DjangoObjectType):
    class Meta:
        model = Month
        fields = "__all__"


class RoundType(DjangoObjectType):
    is_finished = graphene.Boolean()
    current_month_id = graphene.Int()

    def resolve_is_finished(self, info):
        if self.current_month is not None and self.room is not None:
            return self.room.number_of_turns == self.current_month.key
        else:
            return False

    def resolve_current_month_id(self, info):
        return self.current_month.id

    class Meta:
        model = Round
        fields = ["id", "key", "is_active"]


class RoomType(DjangoObjectType):
    code = graphene.String()
    current_round_id = graphene.Int()
    room_owner_id = graphene.Int()
    flow_id = graphene.Int()

    def resolve_code(self, info):
        organization = self.organization
        return f'{organization.prefix}-{str(self.key)}'.upper()

    def resolve_current_round_id(self, info):
        return self.current_round.id
    
    def resolve_room_owner_id(self, info):
        return self.room_owner.id
    
    def resolve_flow_id(self, info):
        return self.flow.id

    class Meta:
        model = Room
        fields = ["id", "key", "__typename", "number_of_turns", "money_per_month"]

class QueueType(DjangoObjectType):
    class Meta:
        model = Queue
        fields = "__all__"