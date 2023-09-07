"""
URL configuration for prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#pylint: disable=no-name-in-module
from django.contrib import admin
from django.urls import path, include
from .views import HomePage

urlpatterns = [    
    path("admin/", admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path("", include('exercise.urls')),
    path("", include('workout.urls')),
    path("", include('workload.urls')),
    path("", include('weight_lifting.urls')),
    path("", include('running.urls')),
]
