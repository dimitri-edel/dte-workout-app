"""URL patterns for workload"""
#pylint: disable=no-name-in-module
from django.urls import path
from .views import RunningList, DeleteRunning


urlpatterns = [    
    path('running-list/<int:workout_exercise_id>',\
        RunningList.as_view(), name='running_list'),
    path('delete-weight-lifting/<int:workout_exercise_id>/<int:exercise_set_id>',\
        DeleteRunning.as_view(), name='delete_running'),
]
