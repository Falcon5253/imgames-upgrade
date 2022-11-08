import graphene
from apps.rooms.models import CardChoice, Winner, Turn, Month, Round, Room, RoomParticipant
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

    def resolve_is_finished(self, info):
        if self.current_month is not None and self.room is not None:
            return self.room.number_of_turns == self.current_month.key
        else:
            return False

    class Meta:
        model = Round
        fields = "__all__"


class RoomType(DjangoObjectType):
    code = graphene.String()

    def resolve_code(self, info):
        organization = self.organization
        return f'{organization.prefix}-{str(self.key)}'.upper()

    class Meta:
        model = Room
        fields = "__all__"
