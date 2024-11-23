from django.urls import path, include

from djangoRecipes.common import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:recipe_id>/', include([
        path('like', views.like_functionality, name='like'),
        path('comment/', include([
            path('', views.CommentCreateView.as_view(), name='comment'),
            path('<int:comment_id>/', views.CommentEditDeleteView.as_view(), name='edit-delete-comment'),

        ])),

    ])),

]
