# Generated by Django 2.1.5 on 2020-02-08 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200207_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_date',
            new_name='start_date',
        ),
    ]
