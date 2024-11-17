from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from djangoRecipes.common.forms import CommentForm
from djangoRecipes.recipes.forms import BaseRecipeForm
from djangoRecipes.recipes.models import Recipe


class AddRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = BaseRecipeForm
    template_name = "recipes/add-recipe-view.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user

        return super().form_valid(form)

class RecipesDashboard(ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]

        return context

class RecipeDetailsView(DetailView):
    model = Recipe
    template_name = "recipes/recipe-details-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["ingredients"] = context["recipe"].ingredients.split(";")
        context["comment_form"] = CommentForm()
        context["recipe"].has_liked = context["recipe"].likes.filter(user=self.request.user).exists()

        return context
