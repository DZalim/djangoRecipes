from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from djangoRecipes.common.forms import CommentForm, SearchForm
from djangoRecipes.recipes.forms import CreateRecipeForm, EditRecipeForm
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()


class AddRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = CreateRecipeForm
    template_name = "recipes/recipe-form-view.html"

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
    paginate_by = 4

    def get_queryset(self):

        if self.request.user.is_staff:
            queryset = Recipe.objects.filter(is_approved=False)
        else:
            queryset = Recipe.objects.filter(is_approved=True)

        search_query = self.request.GET.get('search_criteria', '').strip()
        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]
        context['search_form'] = SearchForm(self.request.GET)

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


class EditRecipeView(UpdateView):
    model = Recipe
    form_class = EditRecipeForm
    template_name = "recipes/recipe-form-view.html"

    def get_success_url(self):
        return reverse_lazy('own-recipes', kwargs={'pk': self.request.user.pk})


class DeleteRecipeView(DeleteView):
    model = Recipe

    def get_success_url(self):
        return reverse_lazy('own-recipes', kwargs={'pk': self.request.user.pk})


class OwnRecipesView(ListView):
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        queryset = Recipe.objects.filter(user=user)

        search_query = self.request.GET.get('search_criteria', '').strip()
        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]
        context['search_form'] = SearchForm(self.request.GET)

        return context


class FavoriteRecipesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 4

    def get_queryset(self):
        queryset = Recipe.objects.filter(likes__user=self.request.user)

        search_query = self.request.GET.get('search_criteria', '').strip()
        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]
        context['search_form'] = SearchForm(self.request.GET)

        return context

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])


class CommentedRecipesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 4

    def get_queryset(self):
        queryset = Recipe.objects.filter(comments__user=self.request.user).order_by('id').distinct('id')

        search_query = self.request.GET.get('search_criteria', '').strip()
        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]
        context['search_form'] = SearchForm(self.request.GET)

        return context

    def test_func(self):
        return self.request.user.id == int(self.kwargs['pk'])


def approve_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe.is_approved = True
    recipe.save()

    return redirect(request.META.get('HTTP_REFERER'))
