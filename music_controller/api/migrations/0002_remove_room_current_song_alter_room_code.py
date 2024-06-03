# Generated by Django 5.0.6 on 2024-06-03 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='current_song',
        ),
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(default='', max_length=8, unique=True),
        ),
    ]
