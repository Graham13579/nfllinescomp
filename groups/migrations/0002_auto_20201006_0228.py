# Generated by Django 3.1.1 on 2020-10-06 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.CharField(default='', max_length=50)),
                ('underdog', models.CharField(default='', max_length=50)),
                ('line', models.FloatField()),
                ('winner', models.CharField(default='', max_length=50)),
                ('winnerscore', models.IntegerField()),
                ('loser', models.CharField(default='', max_length=50)),
                ('loserscore', models.IntegerField()),
                ('scoredifferential', models.IntegerField()),
                ('playerpick', models.CharField(default=50, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GamePicked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickedteam', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerPick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gamepicked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_picked', to='groups.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerchoosing', to='groups.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='picks',
            field=models.ManyToManyField(through='groups.PlayerPick', to='groups.Game'),
        ),
    ]
