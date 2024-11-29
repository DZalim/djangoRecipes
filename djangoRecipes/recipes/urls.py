from django.urls import path, include

from djangoRecipes.photos import views as photo_views
from djangoRecipes.recipes import views

urlpatterns = [
    path('approved/', views.RecipeDashboardApproved.as_view(), name='approved'),
    path('pending/', views.RecipeDashboardPending.as_view(), name='pending'),
    path('add/', views.AddRecipeView.as_view(), name='add-recipe'),
    path('<int:pk>/', include([
        path('', views.RecipeDetailsView.as_view(), name='recipe-details'),
        path('approve', views.approve_recipe, name='approve-recipe'),
        path('edit', views.EditRecipeView.as_view(), name='edit-recipe'),
        path('delete', views.DeleteRecipeView.as_view(), name='delete-recipe'),
        path('photos/', include([
            path('', photo_views.AddRecipePhotoView.as_view(), name='add-recipe-photo'),
            path('<int:photo_pk>/', include([
                path('delete/', photo_views.DeleteRecipePhotoView.as_view(), name='delete-recipe-photo'),
            ]))
        ])),
    ])),
]

