from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from djangoRecipes.accounts.models import AppUser
from djangoRecipes.common.forms import CommentForm
from djangoRecipes.recipes.forms import BaseRecipeForm
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()


class AddRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = BaseRecipeForm
    template_name = "recipes/add-recipe-view.html"

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})


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


class OwnRecipesView(ListView):
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return Recipe.objects.filter(user=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]

        return context

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])


class FavoriteRecipesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.filter(likes__user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]

        return context

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])


class CommentedRecipesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.filter(comments__user=self.request.user).order_by('id').distinct('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]

        return context

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])
