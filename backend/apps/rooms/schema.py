import graphene
from graphene_django.debug import DjangoDebug
from apps.rooms.mutations import CreateRoom, WriteTurn, StartRound, ReStartRound, ConnectRoom, SendMessage
from apps.rooms.types import RoomType, RoundType, RoomParticipantType, TurnType, WinnerType, MessageType, QueueType, MonthType
from apps.rooms.models import Month, Room, Turn, Round, RoomParticipant, Winner, Message, Queue
import json
from apps.organizations.models import Organization
from graphene_subscriptions.events import CREATED, UPDATED, DELETED
from apps.rooms.tasks import MONTH_EVENT


class Query(graphene.ObjectType):
    debug_rooms = graphene.Field(
        DjangoDebug, name='__debug_rooms')
    room_by_code = graphene.Field(
        RoomType, code=graphene.String(), description='Информация о комнате по коду комнаты')
    rooms_in_organization = graphene.List(
        RoomType, subdomain=graphene.String(), description='Список комнат в организации')
    can_do_step_now_by_code = graphene.Boolean(
        code=graphene.String(), description='Может ли пользователь делать ход в данный момент')
    current_round_by_code = graphene.Field(
        RoundType, code=graphene.String(), description='Информация о текущем раунде по коду комнаты')
    is_room_owner = graphene.Boolean(
        code=graphene.String(), description='Является ли владельцем комнаты')
    room_participants = graphene.List(RoomParticipantType, code=graphene.String(
    ), description='Список участников комнаты')
    turns_from_current_round = graphene.List(TurnType, code=graphene.String(
    ), description='Список ходов пользователя в комнате за текущий раунд')
    winners_from_current_round = graphene.List(WinnerType, code=graphene.String(
    ), description='Список победителей в комнате за текущий раунд')
    get_chat_by_room_code = graphene.List(MessageType, code=graphene.String(), description='Сообщения чата комнаты')
    get_queue_of_room = graphene.List(QueueType, code=graphene.String(), description='Очередь в комнате')
    month_by_id = graphene.Field(MonthType, id=graphene.Int(), description='Месяц')

    def resolve_month_by_id(self, info, id):
        try:
            return Month.objects.get(id=id)
        except Exception as e:
            return None

    def resolve_room_participants(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return RoomParticipant.objects.filter(room=room)
        except Exception as e:
            return None

    def resolve_get_queue_of_room(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return Queue.objects.filter(room=room)
        except Exception as e:
            return None

    def resolve_can_do_step_now_by_code(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                current_round = room.current_round
                current_month = current_round.current_month
                turn = Turn.objects.filter(
                    month=current_month, user=user).count()
                return turn == 0
            else:
                raise Exception('Error code')
        except Exception as e:
            return None

    def resolve_rooms_in_organization(self, info, subdomain):
        try:
            organization = Organization.objects.get(subdomain=subdomain)
            return Room.objects.filter(organization=organization).order_by('-key')
        except Exception as e:
            return None

    def resolve_room_by_code(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) <= 1:
                raise Exception('Error code')
            organization = Organization.objects.get(
                prefix__iexact=code_array[0])
            return Room.objects.get(key=code_array[1], organization=organization)

        except Exception as e:
            return None

    def resolve_current_round_by_code(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return room.current_round
        except Exception as e:
            return None

    def resolve_is_room_owner(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return user == room.room_owner
        except Exception as e:
            return None

    def resolve_turns_from_current_round(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                current_round = room.current_round
                months = Month.objects.filter(round=current_round)
                turns = []
                for month in months:
                    turn = Turn.objects.filter(user=user, month=month)
                    turns += turn
                return turns
        except Exception as e:
            return None

    def resolve_winners_from_current_round(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                current_round = room.current_round
                winners = Winner.objects.filter(round=current_round)
                return winners
                # months = Month.objects.filter(round=current_round)
                # turns = []
                # for month in months:
                #     turn = Turn.objects.filter(user=user, month=month)
                #     turns += turn
                # return turns
        except Exception as e:
            return None

    def resolve_get_chat_by_room_code(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                messages = Message.objects.filter(room=room).order_by("created_at")
            return messages
        except Exception as e:
            print(e)
            return None

class Mutation(graphene.ObjectType):
    create_room = CreateRoom.Field()
    write_turn = WriteTurn.Field()
    start_round = StartRound.Field()
    send_message = SendMessage.Field()
    re_start_round = ReStartRound.Field()
    connect_room = ConnectRoom.Field()


def filter_room_events(event, room):
    try:
        if (event.operation == UPDATED):
            return (isinstance(event.instance, Room) and event.instance.pk == int(room.id))
        else:
            return False
    except Exception as e:
        return False


def filter_room_participants_events(event, room):
    try:
        if event.operation in [UPDATED, CREATED] and isinstance(event.instance, RoomParticipant):
            return (event.instance.room.pk == int(room.id))
        return False
    except Exception as e:
        return False


def filter_round_events(event, current_round):
    try:
        if event.operation in [UPDATED, CREATED]:
            return (event.operation == UPDATED and isinstance(event.instance, Round) and event.instance.pk == int(current_round.id))
        else:
            return False
    except Exception as e:
        return False

def filter_chat_updated_events(event, room):
    try:
        return isinstance(event.instance, Message) and (event.instance.room.pk == int(room.id))
    except Exception as e:
        return False

def filter_queue_updated_events(event, room):
    try:
        return isinstance(event.instance, Queue) and (event.instance.room.pk == int(room.id))
    except Exception as e:
        return False



class Subscription(graphene.ObjectType):
    room_updated = graphene.Field(RoomType, code=graphene.String())
    chat_updated = graphene.Field(MessageType, code=graphene.String())
    current_round_updated = graphene.Field(RoundType, code=graphene.String())
    room_participants_updated = graphene.Field(RoomParticipantType, code=graphene.String())
    queue_updated = graphene.Field(QueueType, code=graphene.String())
    # round_activity_updated = graphene.List(graphene.Boolean, code=graphene.String())

    # Подписка на обновления списка участников комнаты по коду
    def resolve_room_participants_updated(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return self.filter(lambda event: filter_room_participants_events(event, room)).map(lambda event: event.instance)
            else:
                raise Exception('Error code')
        except Exception as e:
            return None

    # Подписка на обновление очереди
    def resolve_queue_updated(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return self.filter(lambda event: filter_queue_updated_events(event, room)).map(lambda event: event.instance)
        except Exception as e:
            return None


    # Подписка на обновление чата
    def resolve_chat_updated(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return self.filter(lambda event: filter_chat_updated_events(event, room)).map(lambda event: event.instance)
        except Exception as e:
            return None

    # Подписка на обновления комнаты по коду
    def resolve_room_updated(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return self.filter(lambda event: filter_room_events(event, room)).map(lambda event: event.instance)
            else:
                raise Exception('Error code')
        except Exception as e:
            return None

    # Подписка на обновление текущего раунда комнаты
    def resolve_current_round_updated(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                current_round = room.current_round
                return self.filter(lambda event: filter_round_events(event, current_round)).map(lambda event: event.instance)
        except Exception as e:
            return None
