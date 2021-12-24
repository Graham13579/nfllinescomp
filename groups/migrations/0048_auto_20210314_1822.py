# Generated by Django 3.1.1 on 2021-03-14 18:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0047_auto_20210312_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='weeksleft',
            field=models.IntegerField(default=16, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)]),
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.CharField(default='Sunday', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Group Description (optional)'),
        ),
        migrations.AlterField(
            model_name='group',
            name='length',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(17)], verbose_name='How many weeks will your group run for? (1-<django.db.models.fields.IntegerField>)'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Group Name'),
        ),
        migrations.AlterField(
            model_name='group',
            name='numplayers',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(25)], verbose_name='What is the maximum number of people who can be in your group? (25 max)'),
        ),
        migrations.AlterField(
            model_name='group',
            name='password',
            field=models.CharField(default='', max_length=20, verbose_name='Group Password'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ppw',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)], verbose_name='How many games will people in your group pick every week? (1-16)'),
        ),
        migrations.AlterField(
            model_name='group',
            name='privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=7, verbose_name='Do you want a public or password protected group?'),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdate',
            field=models.CharField(default='2021-03-14 18:22', max_length=30, verbose_name='Group start date'),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdaydate',
            field=models.CharField(default='Sunday', max_length=20),
        ),
    ]
