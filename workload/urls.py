"""URL patterns for workload"""
#pylint: disable=no-name-in-module
from django.urls import path
from .views import WorkloadList, DeleteWorkload

urlpatterns = [    
    path('edit_exercise_set/<int:workout_exercise_id>',\
        WorkloadList.as_view(), name='workload_list'),
    path('delete_workload/<int:workout_exercise_id>/<int:exercise_set_id>',\
        DeleteWorkload.as_view(), name='delete_workload'),
]