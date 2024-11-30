from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from djangoRecipes.categories.forms import CategoryForm
from djangoRecipes.categories.models import Category
from djangoRecipes.categories.serializers import CategorySerializer
from djangoRecipes.common.permissions import StaffAndSuperUserPermissions, IsStaffOrSuperUser, AnonymousUserPermissions
from djangoRecipes.recipes.views import BaseRecipeDashboardView


class AddCategoryView(AnonymousUserPermissions, StaffAndSuperUserPermissions, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/add-category-view.html"
    success_url = reverse_lazy("list-categories")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user

        return super().form_valid(form)


class CategoryListView(ListView):
    model = Category
    template_name = "categories/list-categories-views.html"
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category_recipes_count = {}

        for category in context['categories']:
            category_recipes_count[category.pk] = category.recipes.filter(is_approved=True).count()

        context['category_recipes_count'] = category_recipes_count

        return context


class CategoryEditDeleteView(UpdateAPIView, DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsStaffOrSuperUser]

    def get_object(self):
        category_id = self.kwargs.get('pk')
        return get_object_or_404(Category, pk=category_id)


class CategoryRecipesView(BaseRecipeDashboardView):

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])

        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = category.recipes.all()
        else:
            queryset = category.recipes.filter(is_approved=True)

        return self.filter_queryset_by_search(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['main_page'] = False

        return context
