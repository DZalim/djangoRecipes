from django.urls import path

from djangoRecipes.recipes import views

urlpatterns = [
    path('add/', views.AddRecipeView.as_view(), name='add-recipe'),

]
