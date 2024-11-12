from django.urls import reverse_lazy
from django.views.generic import CreateView

from djangoRecipes.recipes.forms import BaseRecipeForm
from djangoRecipes.recipes.models import Recipe


class AddRecipeView(CreateView):
    model = Recipe
    form_class = BaseRecipeForm
    template_name = "recipes/add-recipe-view.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user

        return super().form_valid(form)
