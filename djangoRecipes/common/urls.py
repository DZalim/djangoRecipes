from django.urls import path, include

from djangoRecipes.common import views
from djangoRecipes.recipes import views as recipe_views

urlpatterns = [
    path('', recipe_views.RecipesDashboard.as_view(), name='dashboard'),
    path('<int:recipe_id>/', include([
        path('like', views.like_functionality, name='like'),
        path('comment/', include([
            path('', views.CommentCreateView.as_view(), name='comment'),
            path('<int:comment_id>/', views.CommentEditDeleteView.as_view(), name='edit-delete-comment'),

        ])),

    ])),

]
