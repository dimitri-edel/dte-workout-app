"""URL patterns for workload"""
#pylint: disable=no-name-in-module
from django.urls import path
from .views import WorkloadList

urlpatterns = [    
    path('edit_exercise_set/<int:workout_exercise_id>', WorkloadList.as_view(), name='workload_list'),    
]