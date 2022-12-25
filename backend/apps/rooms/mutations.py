import graphene
from .models import Room, Round, Month, Turn, CardChoice, RoomParticipant, Message, Queue

from apps.organizations.models import Organization
from apps.flows.models import Flow, Card
from apps.rooms.types import RoundType, RoomType, TurnType
from apps.rooms.tasks import change_month_in_room


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

                # Если общая ценна карточек больше бюджета на месяц, возвращаем ошибку
                cards_price = 0
                for card_id in cards_id:
                    card = Card.objects.get(pk=card_id)
                    cards_price += card.cost
                if cards_price > room.money_per_month:
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

                # Записываем шаг в очередь
                room_participant = RoomParticipant.objects.get(room=room, user=user)
                try:
                    queue = Queue.objects.get(room=room, participant=room_participant)
                    queue.made_turn = True
                    queue.save()
                except:                  
                    queue = Queue.objects.create(room=room, participant=room_participant, made_turn=False)

                queues = Queue.objects.filter(room=room)
                for queue in queues:
                    # Если есть кто-то, кто не сделал ход, возвращаем результат
                    if queue.made_turn == False:  
                        return WriteTurn(turn=turn, success=True)
                
                # Меняем месяц если все сделали ход
                task = change_month_in_room.delay(room.id)

                # Обнуляем их шаги, если был не последний месяц
                key = current_month.key
                if not (Month.objects.filter(key=key+2, round=current_round).count() == 0):
                    for queue in queues:
                        queue.made_turn = False
                        queue.save()

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
                
                # При начале раунда у каждого игрока в очереди должна быть запись
                participants = RoomParticipant.objects.filter(room=room)
                for participant in participants:
                    Queue.objects.get_or_create(room=room, participant=participant)

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
                    for participant in participants:
                        queue = Queue.objects.get(room=room, participant=participant)
                        queue.made_turn = False
                        queue.save()

                    room.current_round = new_round
                    room.save()
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

                return ConnectRoom(success=True, created=created)
        except Exception as e:
            return ConnectRoom(success=False, errors=[str(e)])
