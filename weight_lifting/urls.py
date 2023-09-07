"""URL patterns for workload"""
#pylint: disable=no-name-in-module
from django.urls import path
from .views import WeightLiftingList, DeleteWeightLifting


urlpatterns = [    
    path('weight-lifting-list/<int:workout_exercise_id>',\
        WeightLiftingList.as_view(), name='weight_lifting_list'),
    path('delete-weight-lifting/<int:workout_exercise_id>/<int:exercise_set_id>',\
        DeleteWeightLifting.as_view(), name='delete_weight_lifting'),
]