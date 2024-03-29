# Generated by Django 3.1.1 on 2021-02-13 00:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0033_auto_20210209_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='cost',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Free', 'Free')], default='Free', max_length=7),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.CharField(default='Saturday', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdate',
            field=models.CharField(default=datetime.datetime(2021, 2, 13, 0, 49, 29, 165293, tzinfo=utc), max_length=20, verbose_name='Group start date'),
        ),
    ]
