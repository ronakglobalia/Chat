# Generated by Django 4.2.6 on 2023-12-26 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textmessage',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='textmessage',
            name='to_user',
        ),
    ]
