from collections import defaultdict
from hashlib import new
from celery import shared_task
from apps.organizations.models import Organization, OrganizationSettings
from apps.rooms.models import Room, Month, Turn, CardChoice, Winner
from apps.flows.models import Stage, Channel, ParameterChange
from apps.computed.models import ChannelComputed, StageComputed
from apps.users.models import User
from apps.computed.schema import prepare_computed_game_data_array
from graphene_subscriptions.events import SubscriptionEvent
from django.forms.models import model_to_dict
from collections import defaultdict
from math import ceil

MONTH_EVENT = 'month_event'


def compute_value(old_value, math_operator, change_value):
    if math_operator == '+':
        return old_value+change_value
    if math_operator == '-':
        return old_value-change_value
    if math_operator == '*':
        return old_value*change_value
    if math_operator == '/':
        return old_value/change_value


@shared_task
def adding_task(x, y):
    return x + y


@shared_task
def change_month_in_room(room_id):
    try:
        room = Room.objects.get(pk=room_id)
        current_round = room.current_round
        old_month = current_round.current_month

        # 1. Записываем в computed начальные значения

        # Получаем набор шагов за прошедший игровой месяц
        old_month_users_turns = Turn.objects.filter(month=old_month)

        # Если месяц был в комнате начальным (шаг игрока №1)
        if old_month.key == 0:

            # TODO: Получаем каналы по умолчанию
            channels = Channel.objects.filter(flow=room.flow)

            # TODO: Получаем этапы по умолчанию
            stages = Stage.objects.filter(flow=room.flow)

            # Для каждого шага-пользователя за месяц
            for turn in old_month_users_turns:
                # Для каждого этапа записываем вычисляемое значение c конверсией по умолчанию
                for stage in stages:
                    StageComputed.objects.create(
                        turn=turn, stage=stage, conversion=stage.conversion)

                # Для каждого канала записываем связку Ход + Этап
                for channel in channels:
                    ChannelComputed.objects.create(
                        turn=turn, channel=channel, cardinal_value=channel.default_value)

        # Если месяц был не начальным
        else:
            prev_old_month = Month.objects.get(
                key=(old_month.key-1), round=current_round)
            prev_old_month_users_turns = Turn.objects.filter(
                month=prev_old_month)

            for prev_turn in prev_old_month_users_turns:
                # Получаем новый шаг
                turn = Turn.objects.get(user=prev_turn.user, month=old_month)

                # Получаем этапы предыдущего шага
                prev_computed_stages = StageComputed.objects.filter(
                    turn=prev_turn)

                # Для каждого этапа предыдущего шага
                for old_computed_stage in prev_computed_stages:
                    # Дублируем запись в вычисляемых значениях со ссылкой на новый ход
                    StageComputed.objects.create(
                        turn=turn, stage=old_computed_stage.stage, conversion=old_computed_stage.conversion)

                # Получаем каналы предыдущего шага
                prev_computed_channels = ChannelComputed.objects.filter(
                    turn=prev_turn)

                # Для каждого канала предыдущего шага
                for old_computed_channel in prev_computed_channels:
                    # Дублируем запись в вычисляемых значениях со ссылкой на новый ход
                    ChannelComputed.objects.create(
                        turn=turn, channel=old_computed_channel.channel, cardinal_value=old_computed_channel.cardinal_value)

        # 2. Для каждого изменения из-за карточек обновляем данные

        # Для каждого шага за последний месяц
        for turn in old_month_users_turns:
            # Получаем набор выборов карточек за ход игрока
            user_card_choices = CardChoice.objects.filter(turn=turn)

            # Для каждого выбора карточек
            for choice in user_card_choices:
                # По карточке в выборе находим все изменения параметров
                parameter_change_list = ParameterChange.objects.filter(
                    card=choice.card)

                # Для каждого изменения параметра
                for parameter_change in parameter_change_list:
                    # Если происходит изменение начального трафика канала
                    if parameter_change.type == "FSVL":
                        # Находим в вычисляемых значениях ChannelComputed
                        computed_channel = ChannelComputed.objects.get(
                            channel=parameter_change.channel, turn=turn)

                        # Изменяем значение трафика
                        computed_channel.cardinal_value = ceil(compute_value(
                            old_value=computed_channel.cardinal_value, math_operator=parameter_change.math_operator, change_value=parameter_change.value))
                        computed_channel.save()

                    # Если происходит изменение конверсии этапа:
                    if parameter_change.type == "CONV":
                        # Находим вычисляемое значение StageComputed
                        computed_stage = StageComputed.objects.get(
                            stage=parameter_change.stage, turn=turn)

                        # Изменяем значение конверсии этапа
                        computed_stage.conversion = round(compute_value(
                            old_value=computed_stage.conversion, math_operator=parameter_change.math_operator, change_value=parameter_change.value), 1)
                        computed_stage.save()

        # Высчитываем следующий номер месяца
        new_key = old_month.key+1

        # TODO: check that the new month is not bigger than the maximum key

        # Находим следующий номер месяца
        new_month = Month.objects.filter(key=new_key, round=current_round)

        # Если нет следующего месяца
        if len(new_month) < 1:
            print('ERROR')
            # TODO: send final
            raise Exception('Error month')
        current_round.current_month = new_month[0]
        current_round.save()

        if Month.objects.filter(key=new_key+1, round=current_round).count() == 0:
            try:
                print('ПОСЛЕДНИЙ МЕСЯЦ!!!')
                rating = defaultdict(int)
                for turn in old_month_users_turns:
                    computed_array = prepare_computed_game_data_array(
                        room=room, user=turn.user)
                    computed_total = computed_array[:-1][0].data[-1]
                    rating[turn.user.id] = int(float(computed_total))
                rating = sorted(rating)

                for i, user_id in enumerate(rating[:3]):
                    place = i + 1
                    user = User.objects.get(pk=user_id)
                    Winner.objects.create(
                        user=user, place=place, round=current_round)
                    print(f'place: {i}, user_id: {user_id}')

                print('ПОСЛЕДНИЙ МЕСЯЦ!!!')
            except Exception as e:
                print('ERROR', e)

        # Отправляем всем событие на обновление состояния комнаты
        # TODO: проверить, что корректно обновляется раунд
        room.current_round = current_round
        month_event = SubscriptionEvent(
            operation=MONTH_EVENT,
            instance=model_to_dict(room))
        print("--> EVENT")
        month_event.send()

        # TODO: send update on
        return new_month[0].key
    except Exception as e:
        print('TASK ERROR -------------------------')
        print(e)
        print('TASK ERROR -------------------------')
        return None
