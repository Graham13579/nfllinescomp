# Generated by Django 3.1.1 on 2021-02-17 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0038_auto_20210214_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='startdaydate',
            field=models.CharField(default='Tuesday', max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.CharField(default='Tuesday', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdate',
            field=models.CharField(default='2021-02-16 23:11', max_length=30, verbose_name='Group start date'),
        ),
    ]
