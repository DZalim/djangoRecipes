from django.urls import path

from djangoRecipes.categories import views

urlpatterns = [
    path('add/', views.AddCategoryView.as_view(), name='add-category'),
    path('all-categories/', views.CategoryListView.as_view(), name="list-categories"),
    path('<int:pk>/', views.CategoryEditDeleteView.as_view(), name='edit-delete-category'),

]
