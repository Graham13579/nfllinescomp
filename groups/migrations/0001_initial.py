# Generated by Django 3.1.1 on 2020-10-04 03:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('privacy', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=7)),
                ('password', models.CharField(default='', max_length=20)),
                ('passwordattempt', models.CharField(default='', max_length=20)),
                ('length', models.CharField(choices=[('One Week', 'One Week'), ('Season-long', 'Season-long')], default='One Week', max_length=11)),
                ('ppw', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)], verbose_name='Number of Picks Per Week')),
                ('numplayers', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Max number of players')),
                ('description', models.TextField(blank=True, default='')),
                ('slug', models.SlugField(allow_unicode=True, default='', unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='groups.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('group', 'user')},
            },
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='groups.Player', to=settings.AUTH_USER_MODEL),
        ),
    ]