# Generated by Django 4.2.11 on 2024-04-18 15:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("WBB", "0007_rename_shot_gravitymeasurement_gravity_center_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="GravityMeasurement",
            new_name="Data",
        ),
    ]