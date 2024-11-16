from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from djangoRecipes.categories.forms import CategoryForm
from djangoRecipes.categories.models import Category


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/add-category-view.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user

        return super().form_valid(form)
