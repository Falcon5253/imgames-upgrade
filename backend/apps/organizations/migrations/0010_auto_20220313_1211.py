# Generated by Django 3.2 on 2022-03-13 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_alter_organization_subdomain'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationsettings',
            name='number_of_turns_max',
            field=models.PositiveIntegerField(default=12, verbose_name='Максимальное количество месяцев в комнате по умолчанию'),
        ),
        migrations.AddField(
            model_name='organizationsettings',
            name='number_participants_max',
            field=models.PositiveIntegerField(default=20, verbose_name='Максимальное количество участников в комнате по умолчанию'),
        ),
        migrations.AlterField(
            model_name='organizationsettings',
            name='number_of_turns_default',
            field=models.PositiveIntegerField(default=3, verbose_name='Количество месяцев в комнате по умолчанию'),
        ),
    ]