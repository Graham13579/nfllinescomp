# Generated by Django 3.1.1 on 2020-11-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0018_auto_20201107_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='gamedate',
        ),
        migrations.AddField(
            model_name='game',
            name='date',
            field=models.CharField(default='', max_length=20, verbose_name='Wednesday'),
        ),
    ]
