# Generated by Django 3.1.1 on 2021-02-11 00:15

import annoying.fields
from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20210211_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
