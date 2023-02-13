from django.db import models
from apps.flows.models import Channel, Stage, StageOfChannel
from apps.rooms.models import Turn
from django.core.validators import MaxValueValidator, MinValueValidator


class ChannelComputed(models.Model):
    channel = models.ForeignKey(
        Channel, verbose_name="Изначальный канал", on_delete=models.CASCADE)
    turn = models.ForeignKey(
        Turn, verbose_name="Шаг пользователя", on_delete=models.CASCADE)
    cardinal_value = models.DecimalField(
        "Входной трафик", decimal_places=2, max_digits=10)

    def __str__(self):
        return f'ChannelComputed #{self.id}'

    class Meta:
        verbose_name = 'Просчитанный канал'
        verbose_name_plural = 'Просчитанные каналы'


class StageComputed(models.Model):
    stage = models.ForeignKey(
        Stage, verbose_name="Изначальный 'этап воронки'", on_delete=models.CASCADE)
    turn = models.ForeignKey(
        Turn, verbose_name="Шаг пользователя", on_delete=models.CASCADE)
    conversion = models.DecimalField(
        "Конверсия", decimal_places=4, max_digits=5, validators=[
            MaxValueValidator(1.0000),
            MinValueValidator(0.0001)
        ])
    # cardinal_value = models.PositiveIntegerField("Входной трафик")

    def __str__(self):
        return f'ChannelComputed #{self.id}'

    class Meta:
        verbose_name = 'Просчитанный этап'
        verbose_name_plural = 'Просчитанные этапы'

class StageOfChannelComputed(models.Model):
    stage_of_channel = models.ForeignKey(StageOfChannel, verbose_name="Принадлежность к стадии", on_delete=models.CASCADE)
    conversion = models.DecimalField(
        "Конверсия канала", decimal_places=4, max_digits=5, validators=[
            MaxValueValidator(1.0000),
            MinValueValidator(0.0001)
        ])
    turn = models.ForeignKey(
        Turn, verbose_name="Шаг пользователя", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Просчитанный этапы канала"
        verbose_name_plural = "Просчитанные этапы каналов"

    def __str__(self):
        return f'Конверсия канала "{str(self.id)}" этапа "{str(self.stage_of_channel)}"'
