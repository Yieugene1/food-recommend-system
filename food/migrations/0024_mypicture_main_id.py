# Generated by Django 4.1 on 2023-05-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0023_qitaguo'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypicture',
            name='main_id',
            field=models.IntegerField(default=''),
        ),
    ]