""" Model classes for the workout app"""
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from django.db import models
from django.contrib.auth.models import User
from exercise.models import Exercise


class Workout(models.Model):
    """Workout session"""

    # The owner of the workout session
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_workout"
    )
    # Name of the session
    name = models.CharField(max_length=200, blank=False)
    # Date on which the session took place
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta data for ordering the objects in a descending order"""

        ordering = ["-date"]

    def __str__(self):
        """String representation of the object"""
        return self.name.name

    @property
    def exercise_list(self):
        """Return a list of WorkoutExercise objects related to this Workout session"""
        return WorkoutExercise.objects.filter(workout=self)


class WorkoutExercise(models.Model):
    """
    WorkoutExercise is a relation between Workout and Exercise.
    It allows to link Exercises to a Workout session
    """

    # The owner of the workout session
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_workout_exercise"
    )
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="workout_workout_exercise"
    )
    # The relationship to an Exercise object
    exercise = models.ForeignKey(
        Exercise, on_delete=models.PROTECT, related_name="exercise_workout_exercise"
    )

    def __str__(self):
        """String representation of the object"""
        return f"{self.workout.name} : {self.exercise.name}"
