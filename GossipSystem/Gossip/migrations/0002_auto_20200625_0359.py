# Generated by Django 2.2.7 on 2020-06-25 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Gossip', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='users',
            new_name='user',
        ),
    ]