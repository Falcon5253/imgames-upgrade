# Generated by Django 3.2.12 on 2022-12-26 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0024_auto_20221226_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='is_old',
            field=models.BooleanField(default=False, verbose_name='Не текущий'),
        ),
    ]