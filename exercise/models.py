""" Model classes for exercise app """
#pylint: disable=E0307
from django.db import models
from django.contrib.auth.models import User

# Constants for types of exercise
WEIGHT_LIFTING = 0
RUNNING = 1
ENDURANCE = 2

EXERCISE_TYPE = (
    (WEIGHT_LIFTING, "Weight-Lifting"),
    (RUNNING, "Running"),
    (ENDURANCE, "Endurance")
)
"""EXERCISE_TYPE is used in class Exercise to identify which type of exercise
 the object represents"""


class Exercise(models.Model):
    """
        A class for the type of exercise, such as push-ups, pull-ups, jogging, etc. 
        The WorkoutSet class is related to this class. A WorkoutSet is for a particular.
        type of exercise. For instance, the user wants to do a set of push-ups. 
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_exercise", default=1)
    """Foreign Key : User that owns the exercise."""
    name = models.CharField(max_length=200, blank=False)
    """Name of the exercise"""
    exercise_type = models.IntegerField(
        choices=EXERCISE_TYPE, default=WEIGHT_LIFTING)
    """Type of exercise. There are only two types: Strength and Cardio which are
        defined in a tupple at the top of this script file
    """
    def __str__(self):
        return self.name
