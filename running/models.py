""" Model for workload performed during each set of an exercise of type Weight-Lifting"""
# pylint: disable=no-name-in-module
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from workout.models import WorkoutExercise


class Running(models.Model):
    """Workload logs results of each set of an exercise during a workout session"""

    # Owner of the workload
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_running"
    )
    # The relationship to the owner object of type WorkoutExercise
    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.CASCADE,
        related_name="workout_exercise_running",
        default=0,
    )
    # The time it took to complete the set, if it is a cardio exercise
    time = models.CharField(
        default="00:00:00:0",
        validators=[
            RegexValidator(
                regex="^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9]$",
                message="The time must be entered like 00:00:00:0 ",
            ),
        ],
    )
    # The distance covered in the amount of time specified in the time field
    distance = models.FloatField(default="0.0")

    def __str__(self):
        return f"{self.workout_exercise.__str__()}"
