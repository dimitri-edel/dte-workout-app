""" UTLs for workout app """
#pylint: disable=no-name-in-module
#pylint: disable=E1101
from django.urls import path
from .views import StartWorkout, EditWorkout


urlpatterns = [    
    path('start_workout/', StartWorkout.as_view(), name='start_workout'),
    path('edit_workout/<int:workout_id>', EditWorkout.as_view(), name='edit_workout'),
]