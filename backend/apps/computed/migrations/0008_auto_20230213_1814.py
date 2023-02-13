# Generated by Django 3.2.12 on 2023-02-13 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computed', '0007_alter_stageofchannelcomputed_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagecomputed',
            name='conversion',
            field=models.DecimalField(decimal_places=4, max_digits=5, validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.01)], verbose_name='Конверсия'),
        ),
        migrations.AlterField(
            model_name='stageofchannelcomputed',
            name='conversion',
            field=models.DecimalField(decimal_places=4, max_digits=5, validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(0.01)], verbose_name='Конверсия канала'),
        ),
    ]
