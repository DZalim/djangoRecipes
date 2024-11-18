from django.contrib.auth.views import LogoutView
from django.urls import path, include

from djangoRecipes.accounts import views
from djangoRecipes.photos import views as photo_views
from djangoRecipes.recipes import views as recipe_views

urlpatterns = [
    path('register/', views.AppUserRegisterView.as_view(), name='register'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('photo/', photo_views.AddUserPhoto.as_view(), name='add-user-photo'),
        path('favorite-recipes', recipe_views.FavoriteRecipesView.as_view(), name='favorite-recipes'),
        path('own-recipes', recipe_views.OwnRecipesView.as_view(), name='own-recipes'),
        path('commented-recipes', recipe_views.CommentedRecipesView.as_view(), name='commented-recipes'),
]))
]
