from django.db import models
from apps.users.models import User
from apps.organizations.models import Organization
from apps.flows.models import Card, Flow

PLACE_SELECTION = [
    ('1', 'I место'),
    ('2', 'II место'),
    ('3', 'III место'),
]


def calculate_room_key(fk):
    present_keys = Room.objects.filter(organization=fk).order_by(
        '-key').values_list('key', flat=True)
    if present_keys:
        return present_keys[0]+1
    else:
        return 1


def calculate_round_key(fk):
    present_keys = Round.objects.filter(room=fk).order_by(
        '-key').values_list('key', flat=True)
    if present_keys:
        return present_keys[0]+1
    else:
        return 1


def calculate_month_key(fk):
    present_keys = Month.objects.filter(round=fk).order_by(
        '-key').values_list('key', flat=True)
    if present_keys:
        return present_keys[0]+1
    else:
        return 0


class Round(models.Model):
    """Раунд"""
    room = models.ForeignKey(
        "Room", related_name="related_room", verbose_name="В комнате", on_delete=models.CASCADE)
    current_month = models.ForeignKey(
        "Month", related_name="current_month", verbose_name="Текущий месяц", on_delete=models.CASCADE, null=True, blank=True)
    key = models.PositiveIntegerField("Порядковый номер раунда в комнате")
    is_active = models.BooleanField("Начался ли", default=False)
    created_at = models.DateTimeField("Создан в", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён в", auto_now=True)

    class Meta:
        verbose_name = 'Раунд'
        verbose_name_plural = 'Раунды'
        unique_together = ("key", "room")

    def __str__(self):
        return f"{str(self.room)}.R{str(self.key)}"

    def save(self, *args, **kwargs):
        if self.key is None:
            key = calculate_round_key(self.room)
            self.key = key
        super(Round, self).save(*args, **kwargs)


class Month(models.Model):
    """Месяц"""
    round = models.ForeignKey(
        "Round", verbose_name="Раунд", on_delete=models.CASCADE)
    key = models.PositiveIntegerField("Порядковый номер месяца в раунде")

    class Meta:
        verbose_name = "Месяц"
        verbose_name_plural = "Месяцы"
        unique_together = ("key", "round")

    def __str__(self):
        return (
            f"{str(self.round.room)}.R"
            + str(self.round.key)
            + ".M"
            + str(self.key)
        )

    def save(self, *args, **kwargs):
        if self.key is None:
            key = calculate_month_key(self.round)
            self.key = key
        super(Month, self).save(*args, **kwargs)


class Turn(models.Model):
    """Ход"""
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    month = models.ForeignKey(
        Month, verbose_name="Месяц", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ход"
        verbose_name_plural = "Ходы"

    def __str__(self):
        return f"Ход #{str(self.month.key)}"


class CardChoice(models.Model):
    """Выбор карточек"""
    card = models.ForeignKey(
        Card, verbose_name="Карточка", on_delete=models.CASCADE)
    turn = models.ForeignKey(
        Turn, verbose_name="Ход", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Выбор карточки"
        verbose_name_plural = "Выборы карточек"

    def __str__(self):
        return str(self.id)


class Winner(models.Model):
    """Победитель"""

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    round = models.ForeignKey(
        Round, verbose_name="Раунд", on_delete=models.CASCADE)
    place = models.CharField(
        verbose_name="Место", max_length=1, choices=PLACE_SELECTION)
    result = models.IntegerField(
        verbose_name="Очки")

    class Meta:
        verbose_name = "Призёр"
        verbose_name_plural = "Призёры"

    def __str__(self):
        return f"Победитель #{str(self.id)}"


class Room(models.Model):
    """Комната"""
    organization = models.ForeignKey(
        Organization, verbose_name="В организации", on_delete=models.CASCADE)
    room_owner = models.ForeignKey(
        User, verbose_name="Создатель комнаты", on_delete=models.CASCADE)
    number_of_turns = models.PositiveIntegerField("Количество шагов")
    current_round = models.ForeignKey(
        "Round", related_name="current_round", verbose_name="Текущий раунд", on_delete=models.CASCADE, null=True, blank=True)
    key = models.PositiveIntegerField("Порядковый номер комнаты в организации")
    money_per_month = models.PositiveIntegerField("Бюджет на месяц")
    flow = models.ForeignKey(
        Flow, related_name="flow", verbose_name="Механика комнаты", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        unique_together = ("key", "organization")

    def __str__(self):
        return f'{str(self.organization.prefix)}-{str(self.key)}'.upper()

    def save(self, *args, **kwargs):
        if self.key is None:
            key = calculate_room_key(self.organization)
            self.key = key
        super(Room, self).save(*args, **kwargs)


class RoomParticipant(models.Model):
    """Участник комнаты"""
    room = models.ForeignKey(
        Room, verbose_name="Комната", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Участник комнаты"
        verbose_name_plural = "Участники комнаты"

    def __str__(self):
        return f"Участник #{str(self.id)}"


class Queue(models.Model):
    """Очередь комнаты"""
    room = models.ForeignKey(
        Room, verbose_name="Комната", on_delete=models.CASCADE)
    participant = models.ForeignKey(RoomParticipant, verbose_name="Участник", on_delete=models.CASCADE)
    made_turn = models.BooleanField(verbose_name="Ход сделан", default=False)
    class Meta:
        verbose_name = "Участник в очереди"
        verbose_name_plural = "Участники в очереди"


class Message(models.Model):
    """"Сообщения"""
    room = models.ForeignKey(
        Room, verbose_name="Комната", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField (verbose_name='Текст')
    created_at = models.DateTimeField("Время отправления", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"