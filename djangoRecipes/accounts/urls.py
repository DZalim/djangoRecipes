from django.contrib.auth.views import LogoutView
from django.urls import path

from djangoRecipes.accounts import views

urlpatterns = [
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]
