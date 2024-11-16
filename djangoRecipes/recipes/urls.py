from django.urls import path, include

from djangoRecipes.recipes import views

urlpatterns = [
    path('add/', views.AddRecipeView.as_view(), name='add-recipe'),
    path('dashboard/', views.RecipesDashboard.as_view(), name='dashboard'),
    path('<int:pk>/', include([
        path('', views.RecipeDetailsView.as_view(), name='recipe-details'),
    ])),
]
