# Generated by Django 4.1 on 2023-04-10 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_userinfo1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo1',
            old_name='name1',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='userinfo1',
            old_name='password1',
            new_name='password',
        ),
    ]