from django.db import models
from apps.organizations.models import Organization
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django import forms

MATH_OPERATOR_SELECTION = [
    ('+', '[+] Сложение'),
    ('-', '[-] Вычитание'),
    ('*', '[*] Умножение'),
    ('/', '[/] Деление'),
]

CHANGE_TYPES_SELECTION = [
    ('FSVL', 'Изменение начального значения'),
    # ('AVCH', 'Изменение среднего чека'),
    ('CONV', 'Изменение конверсии'),
]


class ParameterChange(models.Model):
    """Изменение параметра"""
    card = models.ForeignKey(
        "Card", verbose_name="Принадлежность к карточке", on_delete=models.CASCADE)
    channel = models.ForeignKey(
        "Channel", verbose_name="Изменяемый канал", on_delete=models.CASCADE)
    stage = models.ForeignKey(
        "Stage", verbose_name="Изменяемый этап", on_delete=models.CASCADE)
    math_operator = models.CharField(
        verbose_name="Математический оператор", max_length=1, choices=MATH_OPERATOR_SELECTION)
    value = models.DecimalField(
        "Дельта (изменяемое значение)", decimal_places=2, max_digits=10)
    month_of_application = models.PositiveIntegerField(
        "На какой месяц применять")
    type = models.CharField(
        verbose_name="Тип изменений", max_length=4, choices=CHANGE_TYPES_SELECTION)

    class Meta:
        verbose_name = "Изменение параметра"
        verbose_name_plural = "Изменения параметров"

    def __str__(self):
        return f"Изменение параметра #{str(self.id)}"


class StageInSequence(models.Model):
    """Место в последовательности этапов"""
    stage = models.OneToOneField(
        "Stage", verbose_name="Изменяемый этап", on_delete=models.CASCADE)
    place = models.PositiveIntegerField("Место")

    class Meta:
        verbose_name = "Место в последовательности этапов"
        verbose_name_plural = "Места в последовательности этапов"

    def __str__(self):
        return f"(#{str(self.id)})"


class Stage(models.Model):
    """Этап"""
    flow = models.ForeignKey("Flow", verbose_name="Принадлежность к механике",
                            on_delete=models.CASCADE)
    name = models.CharField("Название этапа", max_length=255)
    conversion = models.DecimalField(
        "Стандартная конверсия на этапе", decimal_places=4, max_digits=5, validators=[
            MaxValueValidator(1.0000),
            MinValueValidator(0.0001)
        ])

    class Meta:
        verbose_name = "Этап воронки"
        verbose_name_plural = "Этапы воронки"

    def __str__(self):
        return "'"+self.name+"'"+" (#"+str(self.id)+")"

    def save(self, *args, **kwargs):
        stages_in_flow = Stage.objects.filter(flow=self.flow)
        print('stages_in_flow', stages_in_flow)


        if self not in stages_in_flow:
            new_place = 1
            if len(stages_in_flow) != 0:
                new_place = 2
                for stage in stages_in_flow:
                    stage_in_sequence = StageInSequence.objects.filter(
                        stage=stage).first()
                    print('stage_in_sequence', stage_in_sequence)
                    if stage_in_sequence is not None:
                        print('stage_in_sequence is not None')
                        if stage_in_sequence.place >= new_place:
                            new_place = stage_in_sequence.place+1
                            print('stage_in_sequence.place+1', new_place)
            super(Stage, self).save(*args, **kwargs)
            StageInSequence.objects.get_or_create(
                stage=self, place=new_place)
        else:
            super(Stage, self).save(*args, **kwargs)


class Channel(models.Model):
    """Канал"""
    flow = models.ForeignKey("Flow", verbose_name="Принадлежность к механике",
                            on_delete=models.CASCADE)
    name = models.CharField("Название параметра", max_length=255)
    default_value = models.DecimalField(
        "Начальное значение", decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = "Параметр / Канал"
        verbose_name_plural = "Параметры / Каналы"

    def __str__(self):
        return "'"+self.name+"'"+" (#"+str(self.id)+")"


class StageOfChannel(models.Model):
    """Этап для конкретных каналов"""
    stage = models.ForeignKey(Stage, verbose_name="Принадлежность к стадии", on_delete=models.CASCADE)
    conversion = models.DecimalField(
        "Конверсия канала", decimal_places=4, max_digits=5, validators=[
            MaxValueValidator(1.0000),
            MinValueValidator(0.0001)
        ])
    channels = models.ManyToManyField(Channel, blank=True, max_length=255, verbose_name='Принадлежность конверсии к каналам')

    class Meta:
        verbose_name = "Конверсия определенного канала"
        verbose_name_plural = "Конверсии определенных каналов"

    def __str__(self):
        return f'Конверсия канала "{str(self.id)}" этапа "{str(self.stage)}"'


class Card(models.Model):
    """Карточка"""
    flow = models.ForeignKey("Flow", verbose_name="Принадлежность к механике",
                             on_delete=models.CASCADE)
    header = models.CharField("Заголовок", max_length=255)
    short_description = models.TextField("Короткое описание")
    cost = models.PositiveIntegerField(
        "Стоимость")

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        return "'"+self.header+"'"+" (#"+str(self.id)+")"


class Flow(models.Model):
    """Механика"""
    organization = models.ForeignKey(
        Organization, verbose_name="Принадлежит к организации", on_delete=models.CASCADE)
    title = models.CharField("Название механики", max_length=255)

    class Meta:
        verbose_name = "Механика"
        verbose_name_plural = "Механики"

    def __str__(self):
        return f'{self.title} - {str(self.organization)} (#{str(self.pk)})'

# Проверяем, чтобы на одном этапе "этапы канала" не имели общих каналов
class StageOfChannelForm(forms.ModelForm):
    def clean(self):
        channels_id = self.data.getlist('channels')
        stage_id = self.data.get('stage')
        stage = Stage.objects.get(id=stage_id)
        stages_of_channels = StageOfChannel.objects.filter(stage=stage)
        for channel_id in channels_id:

            channel= Channel.objects.get(id=channel_id)
            print(channel)
            stage_of_channel = stages_of_channels.filter(channels=channel)
            if len(stage_of_channel) > 0:
                if stage_of_channel[0] == self.instance:
                    print("Hi me")
                    continue
            if stage_of_channel.exists():
                raise ValidationError("Для выбранного вами канала на выбранной вами стадии конвервия уже была определена")

        # for stage_of_channel in stages_of_channels:
        #     if self.instance == stage_of_channel:
        #         pass
        #     for channel_id in channels_id:
        #         print(stage_of_channel.channels.all())
        # for stage in stages:

        # print(others)

# Проверяем, чтобы имя у этапа было уникальным среди этапов определенной механики
class StageForm(forms.ModelForm):
    def clean(self):
        flow_id = self.data.get('flow')
        name = self.data.get('name')
        flow = Flow.objects.get(id=flow_id)
        stages = Stage.objects.filter(flow=flow)
        for stage in stages:
            if stage.name == name:
                raise ValidationError('Этап с таким именем в выбранной механике уже существует!')