# Generated by Django 4.1 on 2023-05-07 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0014_mypicture_class2_mypicture_country_mypicture_taste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypicture',
            name='intro',
            field=models.CharField(default='', max_length=300),
        ),
    ]
