# Generated by Django 4.2.11 on 2024-04-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WBB", "0011_data_height_data_width"),
    ]

    operations = [
        migrations.AlterField(
            model_name="data",
            name="height",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="data",
            name="width",
            field=models.FloatField(),
        ),
    ]
