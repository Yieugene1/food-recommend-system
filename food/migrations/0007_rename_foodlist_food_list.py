# Generated by Django 4.1 on 2023-04-08 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_rename_food_list_foodlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Foodlist',
            new_name='food_list',
        ),
    ]