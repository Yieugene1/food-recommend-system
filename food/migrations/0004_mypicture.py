# Generated by Django 4.1 on 2023-04-08 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_food_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='mypicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('photo', models.ImageField(default='user1.jpg', upload_to='photos')),
            ],
        ),
    ]
