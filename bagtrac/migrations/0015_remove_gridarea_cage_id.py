# Generated by Django 4.2.5 on 2023-12-30 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrac', '0014_gridarea_is_assigned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gridarea',
            name='cage_id',
        ),
    ]
