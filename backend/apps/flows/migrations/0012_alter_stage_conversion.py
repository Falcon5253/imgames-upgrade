# Generated by Django 3.2.12 on 2022-12-19 16:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0011_auto_20221219_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='conversion',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MaxValueValidator(100.0), django.core.validators.MinValueValidator(0.01)], verbose_name='Стандартная конверсия на этапе'),
        ),
    ]
