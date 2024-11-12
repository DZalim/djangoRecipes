from django.urls import path

from djangoRecipes.categories import views

urlpatterns = [
    path('add/', views.AddCategoryView.as_view(), name='add-category'),

]
