# Generated by Django 4.1 on 2023-04-10 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_alter_mypicture_method1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name1', models.CharField(max_length=32)),
                ('password1', models.CharField(max_length=64)),
                ('hobby1', models.CharField(default='', max_length=64)),
                ('hobby2', models.CharField(default='', max_length=64)),
                ('hobby3', models.CharField(default='', max_length=64)),
            ],
        ),
    ]
