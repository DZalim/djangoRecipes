from django.urls import path, include

from djangoRecipes.common import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('like/<int:recipe_id>/', views.like_functionality, name='like'),
    path('comment/<int:recipe_id>/', views.comment_functionality, name='comment'),
]
