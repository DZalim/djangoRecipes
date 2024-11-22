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
        path('edit/', views.EditProfileView.as_view(), name='edit-profile'),
        path('delete/', views.DeleteProfileView.as_view(), name='delete-profile'),
        path('photo/', include([
            path('', photo_views.AddUserPhotoView.as_view(), name='add-user-photo'),
            path('<int:photo_pk>/', include ([
                path('edit/', photo_views.ChangeUserPhotoView.as_view(), name='change-user-photo'),
                path('delete/', photo_views.DeleteUserPhotoView.as_view(), name='delete-user-photo'),

            ])),

        ])),

        path('favorite-recipes', recipe_views.FavoriteRecipesView.as_view(), name='favorite-recipes'),
        path('own-recipes', recipe_views.OwnRecipesView.as_view(), name='own-recipes'),
        path('commented-recipes', recipe_views.CommentedRecipesView.as_view(), name='commented-recipes'),
]))
]
