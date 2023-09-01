""" UTLs for Exercise app """
#pylint: disable=no-name-in-module
from django.urls import path
from .views import ExerciseList, EditExercise, CreateExercise


#pylint: disable=E1101
urlpatterns = [    
    path('exercise-list/', ExerciseList.as_view(), name='exercise_list'),
    path('create_exercise/', CreateExercise.as_view(), name='create_exercise'),
    path('exercise/<int:exercise_id>', EditExercise.as_view(), name='edit_exercise'),
]