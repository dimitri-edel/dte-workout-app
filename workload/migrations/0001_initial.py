# Generated by Django 4.2.2 on 2023-09-04 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("workout", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Workload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reps", models.IntegerField(blank=True, default="0", null=True)),
                ("weight", models.IntegerField(blank=True, default="0", null=True)),
                ("time", models.CharField(blank=True, default="00:00:00:0", null=True)),
                ("distance", models.FloatField(blank=True, default="0", null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner_workload",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workout_exercise",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workout_exercise_exercise_set",
                        to="workout.workoutexercise",
                    ),
                ),
            ],
        ),
    ]
