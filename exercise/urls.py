""" UTLs for Exercise app """
#pylint: disable=no-name-in-module
from django.urls import path
from .views import HomePage, ExerciseList, EditExercise

#pylint: disable=E1101
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('exercise-list/', ExerciseList.as_view(), name='exercise_list'),
    path('exercise/<int:exercise_id>', EditExercise.as_view(), name='edit_exercise'),
]