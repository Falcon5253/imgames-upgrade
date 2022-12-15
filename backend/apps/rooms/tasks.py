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
        prev_month = current_round.current_month

        # 1. Записываем в computed начальные значения

        # Получаем набор шагов за прошедший игровой месяц
        prev_month_users_turns = Turn.objects.filter(month=prev_month).order_by('id')

        # Если месяц был в комнате начальным (шаг игрока №1)
        if prev_month.key == 0:

            # TODO: Получаем каналы по умолчанию
            channels = Channel.objects.filter(flow=room.flow)

            # TODO: Получаем этапы по умолчанию
            stages = Stage.objects.filter(flow=room.flow)

            # Для каждого шага-пользователя за месяц
            for turn in prev_month_users_turns:
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
                key=(prev_month.key-1), round=current_round)
            prev_old_month_users_turns = Turn.objects.filter(
                month=prev_old_month)

            for prev_turn in prev_old_month_users_turns:
                # Получаем новый шаг
                turn = Turn.objects.get(user=prev_turn.user, month=prev_month)

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

            
        # Находим ходы за предыдущие месяца для проверки месяца применения карточек
        all_turns_of_user = []
        all_months = Month.objects.filter(round=current_round)
        print(all_months)
        for month in all_months:
            try:
                turn = Turn.objects.get(user=turn.user, month=month)
                all_turns_of_user = [turn] + all_turns_of_user
                print("id шагов:")
                print(turn.id)
            except Turn.DoesNotExist:
                pass
        print("конец id шагов")


        # Проверка предыдущих месяцев
        previous_turn_in_row = {}
        # Получаем все ходы пользователя
        for turn in all_turns_of_user:
            print("ХОД!!!!!")
            current_turn_in_row = {}
            user_card_choices = CardChoice.objects.filter(turn=turn)
            # Получаем все выборы карт в ходе пользователя
            for card_choice in user_card_choices:
                current_turn_in_row.update({ card_choice.card.id: 1 })
                if card_choice.card.id in previous_turn_in_row:
                    current_turn_in_row[card_choice.card.id] += previous_turn_in_row[card_choice.card.id]
                print("Шаги подряд")
                print(previous_turn_in_row)
                print(current_turn_in_row)
            # Запоминаем, сколько раз подряд карточки применялись
            previous_turn_in_row = current_turn_in_row  


        # 2. Для каждого изменения из-за карточек обновляем данные
        # Для каждого шага за последний месяц
        for turn in prev_month_users_turns:
            # Получаем набор выборов карточек за ход игрока
            user_card_choices = CardChoice.objects.filter(turn=turn)

            # Для каждого выбора карточек
            for choice in user_card_choices:
                # По карточке в выборе находим все изменения параметров
                parameter_change_list = ParameterChange.objects.filter(
                    card=choice.card)

                # Для каждого изменения параметра
                for parameter_change in parameter_change_list:
                    # Если месяц применения не равен текущему месяцу или не равен нулю, то пропускаем карточку.
                    print(111111)
                    print(previous_turn_in_row)
                    print(previous_turn_in_row[choice.card.id])
                    print(parameter_change.month_of_application)
                    if previous_turn_in_row[choice.card.id] < parameter_change.month_of_application:
                        continue
                    print(222222)
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
        new_key = prev_month.key+1

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

        # Если последний месяц
        if Month.objects.filter(key=new_key+1, round=current_round).count() == 0:
            try:
                total_points = {}
                all_month_of_the_round = Month.objects.filter(round=current_round).order_by('id')
                
                # Ищем сумму финальных очков за предыдущие месяца
                for month in all_month_of_the_round:
                    turn_of_the_month =  Turn.objects.filter(month=month).order_by('id')

                    for turn in turn_of_the_month:
                        computed_array = prepare_computed_game_data_array(
                            user=turn.user, room=room, current_month=month)
                        if turn.user.id not in total_points.keys():
                            total_points[turn.user.id] = 0.00
                        total_points[turn.user.id] += float(computed_array[-1].data[-1])

                # Добавляем очки за следующие месяца
                print('ПОСЛЕДНИЙ МЕСЯЦ!!!')
                for turn in prev_month_users_turns:
                    computed_array = prepare_computed_game_data_array(
                        room=room, user=turn.user)

                    if turn.user.id not in total_points.keys():
                        total_points[turn.user.id] = 0.00
                    total_points[turn.user.id] += float(computed_array[-1].data[-1])

                # Сортируем по значениям
                sorted_total_points = {}
                sorted_values = []

                for value in total_points.values():
                    sorted_values += [int(value)]
                    sorted_values = sorted(sorted_values)

                for i in sorted_values:
                    for k in total_points.keys():
                        if total_points[k] == i:
                            sorted_total_points[k] = total_points[k]
                            break
                        
                place = 0
                # Заполнить победителей в БД
                for user_id in total_points:
                    place += 1
                    if place > 3:
                        break
                    user = User.objects.get(pk=user_id)
                    result = total_points[user_id]
                    Winner.objects.create(
                        user=user, place=place, round=current_round, result=result)
                    print(f'place: {place}, user_id: {user_id}')
                    
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
