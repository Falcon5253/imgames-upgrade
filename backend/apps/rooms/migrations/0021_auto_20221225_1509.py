# Generated by Django 3.2.12 on 2022-12-25 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0020_alter_queue_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='made_turn',
            field=models.BooleanField(default=False, verbose_name='Ход сделан'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.roomparticipant', verbose_name='Участник'),
        ),
    ]