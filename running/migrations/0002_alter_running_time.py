# Generated by Django 4.2.2 on 2023-09-13 18:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("running", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="running",
            name="time",
            field=models.CharField(
                default="00:00:00:0",
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_time",
                        message="The time must be entered like 00:00:00:0 ",
                        regex="^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9]$",
                    )
                ],
            ),
        ),
    ]
