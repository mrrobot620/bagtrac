# Generated by Django 4.2.5 on 2024-01-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrac', '0017_alter_data_cage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bags',
            name='seal_id',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]