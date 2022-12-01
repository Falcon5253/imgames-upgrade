from decimal import Decimal
import graphene
from graphene_django.debug import DjangoDebug
from .types import ComputedGameDataType
from .models import ChannelComputed, StageComputed
from apps.organizations.models import Organization
from apps.rooms.models import Room, Turn, Month
from apps.flows.models import Channel, Stage
from apps.users.models import User
from graphene_subscriptions.events import CREATED, UPDATED, DELETED
from math import ceil


def prepare_computed_game_data_array(room, user, current_month=None):
    # Получаем обновлённый объект комнаты
    room = Room.objects.get(pk=room.id)
    if current_month is None:
        current_month = room.current_round.current_month

    # Находим текущий механику комнаты
    flow = room.flow

    # Находим данные о каналах по умолчанию
    channels = Channel.objects.filter(flow=flow)

    # Находим данные о этапах воронки по умолчанию
    stages = Stage.objects.filter(flow=flow).order_by('id')
    answer_array = []
    # Если начальный месяц
    if current_month.key == 0:
        total_data = [Decimal(0)]

        for i in range(len(stages)):
            total_data += [Decimal(0), Decimal(0)]

        for channel in channels:
            # Находим входное значение канала
            channel_start_value = channel.default_value
            data = [channel_start_value]
            total_data[0] += channel_start_value

            # Вычисляем значение для каждого этапа воронки
            channel_next = channel_start_value
            for i, stage in enumerate(stages, start=0):

                # Высчитываем значение после конверсии
                channel_next = ceil(channel_next * stage.conversion)

                #
                total_data[1+(2*i)] = '{0:.2f}'.format(
                    Decimal(total_data[1+(2*i)])+Decimal(0))
                total_data[2+(2*i)] = '{0:.2f}'.format(
                    Decimal(channel_next)+Decimal(total_data[2+(2*i)]))

                # Форматируем данные для ответа
                data += ['{0:.2f}'.format(stage.conversion),
                         '{0:.2f}'.format(channel_next)]

            # Добавляем данные в массив возвращаемых значений
            answer_array += [ComputedGameDataType(
                data=data, channel=channel, is_total=False)]

        # Добавляем значение ИТОГО
        answer_array += [ComputedGameDataType(
            data=total_data, channel=None, is_total=True)]
        # print(total_data)
        return answer_array

    # Если не начальный месяц
    else:
        # Находим предыдущий месяц
        prev_month_key = current_month.key-1
        prev_month = Month.objects.get(
            key=prev_month_key, round=room.current_round)

        # Получаем шаг по пользователю и предыдущему месяцу
        user_turn = Turn.objects.get(
            month=prev_month, user=user)

        # Получаем вычисленные этапы по шагу
        computed_stages = StageComputed.objects.filter(
            turn=user_turn).order_by("stage")

        # Получаем вычисленные каналы по шагу
        computed_channels = ChannelComputed.objects.filter(
            turn=user_turn)

        # Формируем массив для отправки
        total_data = [Decimal(0)]
        for i in range(len(stages)):
            total_data += [Decimal(0), Decimal(0)]

        for computed_channel in computed_channels:

            # Находим входное значение канала
            channel_start_value = Decimal(
                computed_channel.cardinal_value)
            data = [channel_start_value]
            total_data[0] += channel_start_value

            # Вычисляем значение для каждого этапа воронки
            channel_next = channel_start_value
            for i, stage in enumerate(computed_stages, start=0):

                # Высчитываем значение после конверсии
                channel_next = ceil(channel_next * stage.conversion)

                #
                total_data[1+(2*i)] = '{0:.2f}'.format(
                    Decimal(total_data[1+(2*i)])+Decimal(0))
                total_data[2+(2*i)] = '{0:.2f}'.format(
                    Decimal(channel_next)+Decimal(total_data[2+(2*i)]))

                # Форматируем данные для ответа
                data += ['{0:.2f}'.format(stage.conversion),
                         '{0:.2f}'.format(channel_next)]

            # Добавляем данные в массив возвращаемых значений
            answer_array += [ComputedGameDataType(
                data=data, channel=computed_channel.channel, is_total=False, month_key=current_month.key)]

        # Добавляем значение ИТОГО
        answer_array += [ComputedGameDataType(
            data=total_data, channel=None, is_total=True, month_key=current_month.key)]

        return answer_array


class Query(graphene.ObjectType):
    debug_computed = graphene.Field(DjangoDebug, name='__debug_computed')
    computed_channels_by_code = graphene.List(ComputedGameDataType, code=graphene.String(
    ), description='Игровые данные пользователя на текущий месяц по коду комнаты')
    all_computed_months_by_code = graphene.List(ComputedGameDataType, code=graphene.String(
    ), description='Игровые данные пользователя на текущий месяц по коду комнаты')
    all_computed_months_by_code_total = graphene.Int(code=graphene.String(
    ), description='Всего очков набрано пользователем')

    def resolve_computed_channels_by_code(root, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return prepare_computed_game_data_array(room=room, user=user, current_month=room.current_round.current_month)
            else:
                raise Exception('Error code')
        except Exception as e:
            print(e)
            return None

    def resolve_all_computed_months_by_code(root, info, code):
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
                computed_data = []
                for month in months:
                    computed_data += prepare_computed_game_data_array(
                        room=room, user=user, current_month=month)
                return computed_data
            else:
                raise Exception('Error code')
        except Exception as e:
            print(e)
            return None
    
    def resolve_all_computed_months_by_code_total(root, info, code):
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
                total = 0
                for month in months:
                    for channel in prepare_computed_game_data_array(room=room, user=user, current_month=month):
                        if channel.is_total == True:
                            total += int(float(channel.data[-1]))
                return total
            else:
                raise Exception('Error code')
        except Exception as e:
            print(e)
            return None


def filter_room_events(event, room, user):
    try:
        if event.operation in [UPDATED, CREATED] and (isinstance(event.instance, (ChannelComputed, StageComputed))):
            event_turn = event.instance.turn
            # TODO: ограничить по пользователю
            event_month = event_turn.month
            event_round = event_month.round
            event_room = event_round.room
            return event_room.pk == int(room.id)
        return False
    except Exception as e:
        print(e)
        return False


class Subscription(graphene.ObjectType):
    computed_channels_by_code_updated = graphene.List(
        ComputedGameDataType, code=graphene.String(), user_id=graphene.ID())

    def resolve_computed_channels_by_code_updated(self, info, code, user_id):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = User.objects.get(pk=user_id)
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                return self.filter(lambda event: filter_room_events(event=event, room=room, user=user)).map(lambda event: prepare_computed_game_data_array(room=room, user=user))
            else:
                raise Exception('Error code')
        except Exception as e:
            return None


class Mutation(graphene.ObjectType):
    pass
