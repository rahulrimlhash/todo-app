# Generated by Django 4.1 on 2024-10-21 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todoapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
