# Generated by Django 4.1 on 2023-05-16 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0026_remove_mypicture_main_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypicture',
            name='main_id',
            field=models.IntegerField(default=1),
        ),
    ]
