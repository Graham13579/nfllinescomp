# Generated by Django 3.1.1 on 2021-03-09 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0041_auto_20210228_2326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='payoutdate',
            new_name='enddate',
        ),
        migrations.RemoveField(
            model_name='group',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='group',
            name='paidorfree',
        ),
        migrations.RemoveField(
            model_name='group',
            name='pot',
        ),
        migrations.AlterField(
            model_name='game',
            name='gamedate',
            field=models.CharField(default='Tuesday', max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdate',
            field=models.CharField(default='2021-03-09 19:16', max_length=30, verbose_name='Group start date'),
        ),
        migrations.AlterField(
            model_name='group',
            name='startdaydate',
            field=models.CharField(default='Tuesday', max_length=20),
        ),
    ]
