# Generated by Django 5.0.6 on 2024-06-24 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_activity_options_alter_activity_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="activity",
            old_name="public",
            new_name="favorite",
        ),
    ]
