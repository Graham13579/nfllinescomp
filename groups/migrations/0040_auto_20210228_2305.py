# Generated by Django 3.1.1 on 2021-03-01 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0039_auto_20210216_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='payoutdate',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.CharField(default='Sunday', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdate',
            field=models.CharField(default='2021-02-28 23:05', max_length=30, verbose_name='Group start date'),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdaydate',
            field=models.CharField(default='Sunday', max_length=20),
        ),
    ]