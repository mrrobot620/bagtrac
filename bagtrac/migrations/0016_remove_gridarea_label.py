# Generated by Django 4.1 on 2023-12-31 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrac', '0015_remove_gridarea_cage_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gridarea',
            name='label',
        ),
    ]
