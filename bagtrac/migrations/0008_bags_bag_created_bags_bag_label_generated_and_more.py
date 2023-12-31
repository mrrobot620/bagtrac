# Generated by Django 4.1 on 2023-12-26 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bagtrac', '0007_bagstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='bags',
            name='bag_created',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bags',
            name='bag_label_generated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bags',
            name='put_in_grid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bags',
            name='put_out_grid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bags',
            name='recieved_at_cv',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='BagStatus',
        ),
    ]
