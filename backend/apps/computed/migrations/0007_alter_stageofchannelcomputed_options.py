# Generated by Django 3.2.12 on 2022-12-29 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computed', '0006_rename_stageofchannel_stageofchannelcomputed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stageofchannelcomputed',
            options={'verbose_name': 'Просчитанный этапы канала', 'verbose_name_plural': 'Просчитанные этапы каналов'},
        ),
    ]
