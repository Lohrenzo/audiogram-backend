# Generated by Django 5.1 on 2024-09-11 15:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="album",
            old_name="releaded",
            new_name="released",
        ),
    ]
