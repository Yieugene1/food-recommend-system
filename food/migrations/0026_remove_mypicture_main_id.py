# Generated by Django 4.1 on 2023-05-16 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0025_alter_mypicture_main_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mypicture',
            name='main_id',
        ),
    ]