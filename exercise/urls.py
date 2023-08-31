""" UTLs for Exercise app """
from django.urls import path
from . import views

#pylint: disable=E1101
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
]