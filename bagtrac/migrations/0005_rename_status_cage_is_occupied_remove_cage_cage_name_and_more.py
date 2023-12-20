# Generated by Django 4.1 on 2023-12-20 06:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrac', '0004_cage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cage',
            old_name='status',
            new_name='is_occupied',
        ),
        migrations.RemoveField(
            model_name='cage',
            name='cage_name',
        ),
        migrations.AddField(
            model_name='cage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='cage',
            name='cage_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
