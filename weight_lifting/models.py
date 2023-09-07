""" Model for workload performed during each set of an exercise of type Weight-Lifting"""
#pylint: disable=no-name-in-module
from django.db import models
from django.contrib.auth.models import User
from workout.models import WorkoutExercise

class WeightLifting(models.Model):
    """Workload logs results of each set of an exercise during a workout session"""
    # Owner of the workload
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_weight_lifting")
    # The relationship to the owner object of type WorkoutExercise  
    workout_exercise = models.ForeignKey(WorkoutExercise,\
     on_delete=models.CASCADE, related_name="workout_exercise_weight_lifting", default=0)
    # Number of repetitions in this set
    reps = models.IntegerField(blank=True, null=True, default="0")
    # The weight that was used, if weight lifting is involved
    weight = models.IntegerField(blank=True, null=True, default="0")
    
    def __str__(self):
        return f"{self.workout_exercise.__str__()}"
