""" UTLs for workout app """
#pylint: disable=no-name-in-module
#pylint: disable=E1101
from django.urls import path
from .views import StartWorkout, EditWorkout, DeleteWorkoutExercise, WorkoutList


urlpatterns = [    
    path('start_workout/', StartWorkout.as_view(), name='start_workout'),
    path('edit_workout/<int:workout_id>', EditWorkout.as_view(), name='edit_workout'),
    path('delete_workout_exercise/<int:workout_exercise_id>/<int:workout_id>',\
        DeleteWorkoutExercise.as_view(), name='delete_workout_exercise'),
    path('workout_list/', WorkoutList.as_view(), name='workout_list'),
]