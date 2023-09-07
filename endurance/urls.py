"""URL patterns for workload"""
#pylint: disable=no-name-in-module
from django.urls import path
from .views import EnduranceList, DeleteEndurance


urlpatterns = [    
    path('endurance-list/<int:workout_exercise_id>',\
        EnduranceList.as_view(), name='endurance_list'),
    path('delete-endurance/<int:workout_exercise_id>/<int:exercise_set_id>',\
        DeleteEndurance.as_view(), name='delete_endurance'),
]
