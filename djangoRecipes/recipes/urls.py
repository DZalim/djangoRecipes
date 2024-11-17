from django.urls import path, include

from djangoRecipes.recipes import views
from djangoRecipes.photos import views as photo_views

urlpatterns = [
    path('add/', views.AddRecipeView.as_view(), name='add-recipe'),
    path('dashboard/', views.RecipesDashboard.as_view(), name='dashboard'),
    path('<int:pk>/', include([
        path('', views.RecipeDetailsView.as_view(), name='recipe-details'),
        path('photos/', photo_views.AddRecipePhotoView.as_view(), name='add-recipe-photo')
    ])),
]
