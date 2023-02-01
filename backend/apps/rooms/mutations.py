import graphene
from .models import Room, Round, Month, Turn, CardChoice, RoomParticipant, Message
from apps.organizations.models import Organization
from apps.flows.models import Flow, Card
from apps.rooms.types import RoundType, RoomType, TurnType
from apps.rooms.tasks import change_month_in_room
from config.pusher import pusher_client


class CreateRoom(graphene.Mutation):
    """ Мутация для создания комнаты (+ раунда и необходимого количества месяцев) в пространстве организации """
    room = graphene.Field(RoomType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    code = graphene.String()
    round = graphene.Field(RoundType)

    class Arguments:
        subdomain = graphene.String(required=True)
        number_of_turns = graphene.Int(required=True)
        money_per_month = graphene.Int(required=True)
        flow_id = graphene.ID(required=True)

    def mutate(self, info, subdomain, number_of_turns, money_per_month, flow_id):
        try:
            organization = Organization.objects.get(subdomain=subdomain)
            user = info.context.user

            # Находим механику
            flow = Flow.objects.get(pk=flow_id)

            # Создаём новый объект комнаты
            room = Room.objects.create(
                organization=organization, room_owner=user, number_of_turns=number_of_turns, money_per_month=money_per_month, flow=flow)
            code = str(room)

            # Создаём новый раунд в комнате
            new_round = Round.objects.create(room=room)
            room.current_round = new_round
            room.save()

            # Создаём необходимое количество месяцев
            first_month = None
            for _ in range(room.number_of_turns+1):
                if first_month is not None:
                    Month.objects.create(round=new_round)
                else:
                    first_month = Month.objects.create(round=new_round)

            new_round.current_month = first_month
            new_round.save()

            # Добавляем пользователя как участника
            RoomParticipant.objects.create(room=room, user=user)

            return CreateRoom(success=True, room=room, code=code, round=new_round)
        except Exception as e:
            return CreateRoom(success=False, errors=[str(e)])


class WriteTurn(graphene.Mutation):
    """ Мутация для записи шага пользователя в комнате """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    turn = graphene.Field(TurnType)

    class Arguments:
        code = graphene.String(required=True)
        cards_id = graphene.List(graphene.ID, required=True)

    def mutate(self, info, code, cards_id):
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
                
                
                # Считаем бюджет на данный месяц
                months = Month.objects.filter(round=current_round)
                turns = []
                expenses = 0
                for month in months:
                    turns += Turn.objects.filter(user=user, month=month)
                for turn in turns:
                    choices = CardChoice.objects.filter(turn=turn)
                    for choice in choices:
                        card = choice.card
                        expense = card.cost
                        expenses += expense
                months_passed = current_month.key
                
                if months_passed == 0:
                    balance = room.money_per_month
                else:
                    balance = room.money_per_month * (months_passed + 1)
                    balance = balance - expenses

                # Если общая ценна карточек больше бюджета на месяц, возвращаем ошибку
                cards_price = 0
                for card_id in cards_id:
                    card = Card.objects.get(pk=card_id)
                    cards_price += card.cost
                    
                if cards_price > balance:
                    raise Exception('Cards price is bigger than money given per month')

                # Если шаг существует, возвращаем ошибку
                turn = Turn.objects.filter(
                    month=current_month, user=user).count()
                if turn != 0:
                    raise Exception('Turn exists!')

                # Если не существовал такой ход, тогда создаём
                turn = Turn.objects.create(
                    month=current_month, user=user)

                # Для каждой карточки фиксируем выбор
                for card_id in cards_id:
                    card = Card.objects.get(pk=card_id)
                    CardChoice.objects.create(card=card, turn=turn)

                # Участники комнаты и участники комнаты, которые сделали ход
                all_participants = RoomParticipant.objects.filter(room=room)
                turn_made_participants = RoomParticipant.objects.filter(room=room, is_turn_made=True)

                # Проверяем все ли другие сделали ход
                # количество участников сделавших ход должно быть на 1 меньше, чем участников всего
                if turn_made_participants.count() >= (all_participants.count()-1):
                    # Обнуляем их шаги, если был не последний месяц
                    key = current_month.key
                    if not (Month.objects.filter(key=key+2, round=current_round).count() == 0):
                        turn_made_participants.update(is_turn_made=False)

                    # Завершаем раунд, если был последний месяц
                    else:
                        current_participant = all_participants.get(user=user)
                        current_participant.is_turn_made = True
                        current_participant.save()
                        current_round_update = Round.objects.get(id=current_round.id)
                        current_round_update.is_finished = True
                        current_round_update.save()
                    
                    # Меняем месяц
                    task = change_month_in_room.delay(room.id)
                    pusher_client.trigger(room.code, 'roundUpdate', {})

                # Если не все, то записываем, что текущий участник сделал ход
                else:

                    current_participant = all_participants.get(user=user)
                    print(current_participant.is_turn_made)
                    current_participant.is_turn_made = True
                    current_participant.save()
                    print(current_participant.is_turn_made)

                print(1)
                pusher_client.trigger(code, 'participantsUpdate', {})
                print(2)
                # Возвращаем результат
                return WriteTurn(turn=turn, success=True)
            return WriteTurn(success=False, errors=['Error code!'])
        except Exception as e:
            return WriteTurn(success=False, errors=[str(e)])


class StartRound(graphene.Mutation):
    """ Мутация для старта раунда комнаты в пространстве организации """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        code = graphene.String(required=True)

    def mutate(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                if room.room_owner == user:
                    current_round = room.current_round
                    if current_round.is_active:
                        raise Exception('Already started!')
                    current_round.is_active = True
                    current_round.save()

                    # Так отправится запрос roomParticipantUpdated
                    current_participant_filter = RoomParticipant.objects.filter(room=room, user=user)
                    current_participant_filter.update(is_turn_made=True)
                    current_participant_update = RoomParticipant.objects.get(room=room, user=user)
                    current_participant_update.is_turn_made = False
                    current_participant_update.save()
                
                print(3)
                pusher_client.trigger(code, 'roundUpdate', {})
                print(4)
                return StartRound(success=True)
        except Exception as e:
            return StartRound(success=False, errors=[str(e)])

class SendMessage(graphene.Mutation):
    """ Мутация отправки сообщения внутри комнаты """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        code = graphene.String(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, code, text):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                Message.objects.create(room=room, user=user, text=text)
                return SendMessage(success=True)
        except Exception as e:
            print(e)
            return SendMessage(success=False, errors=[str(e)])

class ReStartRound(graphene.Mutation):
    """ Мутация для начала нового раунда комнаты в пространстве организации """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        code = graphene.String(required=True)

    def mutate(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)
                if room.room_owner == user:
                    # Создаём новый раунд в комнате
                    new_round = Round.objects.create(room=room)

                    # Создаём необходимое количество месяцев
                    first_month = None
                    for _ in range(room.number_of_turns+1):
                        if first_month is not None:
                            Month.objects.create(round=new_round)
                        else:
                            first_month = Month.objects.create(round=new_round)
                    
                    new_round.current_month = first_month
                    new_round.save()

                    # Обнуляем ходы в очереди у участников
                    participants = RoomParticipant.objects.filter(room=room)
                    participants.update(is_turn_made=False)

                    old_round = room.current_round
                    old_round.save()

                    room.current_round = new_round
                    room.save()
                # pusher_client.trigger(code, 'roundUpdate', {})
                pusher_client.trigger(code, 'roomUpdate', {})
                return ReStartRound(success=True)
        except Exception as e:
            return ReStartRound(success=False, errors=[str(e)])


class ConnectRoom(graphene.Mutation):
    """ Мутация для присоединения к комнате """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    created = graphene.Boolean()

    class Arguments:
        code = graphene.String(required=True)

    def mutate(self, info, code):
        try:
            code_array = str(code).split('-')
            if len(code_array) > 1:
                user = info.context.user
                organization = Organization.objects.get(
                    prefix__iexact=code_array[0])
                room = Room.objects.get(
                    key=code_array[1], organization=organization)

                participant, created = RoomParticipant.objects.get_or_create(
                    room=room, user=user)
                pusher_client.trigger(code, 'participantsUpdate', {})
                return ConnectRoom(success=True, created=created)
        except Exception as e:
            return ConnectRoom(success=False, errors=[str(e)])
