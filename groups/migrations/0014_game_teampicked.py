# Generated by Django 3.1.1 on 2020-10-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0013_auto_20201012_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='teampicked',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
