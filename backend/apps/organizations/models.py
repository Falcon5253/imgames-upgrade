from django.db import models


class OrganizationSettings(models.Model):
    """Настроки организации"""
    organization = models.OneToOneField(
        "Organization", verbose_name="Организация", on_delete=models.CASCADE, unique=True)
    number_of_turns_default = models.PositiveIntegerField(
        "Количество месяцев в комнате по умолчанию", default=3)
    number_of_turns_max = models.PositiveIntegerField(
        "Максимальное количество месяцев в комнате по умолчанию", default=12)
    number_participants_max = models.PositiveIntegerField(
        "Максимальное количество участников в комнате по умолчанию", default=20)
    money_per_month_default = models.PositiveIntegerField(
        "Количество денег в месяц в комнате по умолчанию", default=10000)

    class Meta:
        verbose_name = "Настройки организации"
        verbose_name_plural = "Настройки организаций"

    def __str__(self):
        return "Настройки организации '"+str(self.organization.name)+"'"


# Организация
class Organization(models.Model):
    organization_owner = models.ForeignKey(
        "users.User", verbose_name="Владелец организации", on_delete=models.CASCADE)
    name = models.CharField("Название пространства", max_length=255)
    subdomain = models.CharField("Поддомен", max_length=50)
    prefix = models.CharField("Префикс комнат", max_length=10)
    created_at = models.DateTimeField("Создано в", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено в", auto_now=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name
