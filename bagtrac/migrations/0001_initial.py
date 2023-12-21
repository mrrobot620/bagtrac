# Generated by Django 4.1 on 2023-12-21 09:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cage_name', models.CharField(max_length=10, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_occupied', models.BooleanField(default=False)),
                ('last_used', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cvs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time1', models.DateTimeField(auto_now_add=True)),
                ('cv', models.CharField(max_length=20)),
                ('bag_seal_id', models.CharField(max_length=255, unique=True)),
                ('user', models.CharField(max_length=255)),
                ('cage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bagtrac.cage')),
            ],
        ),
    ]
