# Generated by Django 4.1 on 2023-05-13 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0020_rename_user_photo_user_save_food_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivation',
            name='food_comment',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='user_save',
            name='score',
            field=models.CharField(default='', max_length=64),
        ),
    ]
