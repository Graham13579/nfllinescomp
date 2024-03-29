# Generated by Django 3.1.1 on 2020-10-10 13:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_group_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['score']},
        ),
        migrations.AddField(
            model_name='playerpick',
            name='pickscoretoadd',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='group',
            name='passwordattempt',
            field=models.CharField(default='a', max_length=20),
        ),
    ]
