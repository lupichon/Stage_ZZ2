# Generated by Django 4.2.11 on 2024-04-19 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WBB", "0010_remove_data_shot_number_data_shot_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="data",
            name="height",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="data",
            name="width",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
