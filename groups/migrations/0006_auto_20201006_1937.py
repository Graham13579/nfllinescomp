# Generated by Django 3.1.1 on 2020-10-06 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20201006_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='loserscore',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='winnerscore',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='playerpick',
            unique_together={('gamepicked', 'player')},
        ),
    ]
