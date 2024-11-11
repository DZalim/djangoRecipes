from django.urls import path, include

from djangoRecipes.common import views

urlpatterns = [
    path('', views.home_view, name='home'),
]
