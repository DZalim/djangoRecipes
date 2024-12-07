from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from djangoRecipes.common.forms import CommentForm, SearchForm
from djangoRecipes.common.permissions import StaffAndSuperUserPermissions, SameUserPermissions
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

        if self.request.user.is_staff or self.request.user.is_superuser:
            recipe.is_approved = True

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('own-recipes', kwargs={'pk': self.request.user.pk})


class BaseRecipeDashboardView(ListView):
    model = Recipe
    template_name = "recipes/dashboard.html"
    context_object_name = 'recipes'
    paginate_by = 4

    def filter_queryset_by_search(self, queryset):
        search_query = self.request.GET.get('search_criteria', '').strip()

        if search_query:
            return queryset.filter(recipe_name__icontains=search_query)

        return queryset

    def get_queryset(self):
        queryset = Recipe.objects.all()
        return self.filter_queryset_by_search(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = context["page_obj"]
        context['search_form'] = SearchForm(self.request.GET)
        context["main_page"] = True
        return context


class RecipesDashboard(BaseRecipeDashboardView):
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()

        queryset = Recipe.objects.filter(is_approved=True)
        return self.filter_queryset_by_search(queryset)


class RecipeDashboardApproved(StaffAndSuperUserPermissions, BaseRecipeDashboardView):

    def get_queryset(self):
        queryset = Recipe.objects.filter(is_approved=True)
        return self.filter_queryset_by_search(queryset)


class RecipeDashboardPending(StaffAndSuperUserPermissions, BaseRecipeDashboardView):

    def get_queryset(self):
        queryset = Recipe.objects.filter(is_approved=False)
        return self.filter_queryset_by_search(queryset)


class RecipeDetailsView(DetailView):
    model = Recipe
    template_name = "recipes/recipe-details-view.html"
    context_object_name = 'recipe'

    def get_object(self, queryset=None):

        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        user = self.request.user

        if not recipe.is_approved:

            if not user.is_authenticated:
                raise Http404

            if user.pk != recipe.user.pk and not (user.is_staff or user.is_superuser):
                raise Http404

        return recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["ingredients"] = context["recipe"].ingredients.split(";")
        context["comment_form"] = CommentForm()

        user = self.request.user
        if user.is_authenticated:
            context["recipe"].has_liked = context["recipe"].likes.filter(user=user).exists()

        return context


class EditRecipeView(SameUserPermissions, UpdateView):
    model = Recipe
    form_class = EditRecipeForm
    template_name = "recipes/recipe-form-view.html"

    def get_success_url(self):
        return reverse_lazy('own-recipes', kwargs={'pk': self.request.user.pk})


class DeleteRecipeView(SameUserPermissions, DeleteView):
    model = Recipe

    def get_success_url(self):
        return reverse_lazy('own-recipes', kwargs={'pk': self.request.user.pk})


class OwnRecipesView(BaseRecipeDashboardView):

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])

        if (self.request.user.id == self.kwargs['pk']
                or self.request.user.is_staff
                or self.request.user.is_superuser):
            queryset = Recipe.objects.filter(user=user)
        else:
            queryset = Recipe.objects.filter(user=user, is_approved=True)

        return self.filter_queryset_by_search(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_page"] = False

        return context


class FavoriteRecipesView(SameUserPermissions, BaseRecipeDashboardView):

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        queryset = Recipe.objects.filter(likes__user=user)

        return self.filter_queryset_by_search(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_page"] = False

        return context


class CommentedRecipesView(SameUserPermissions, BaseRecipeDashboardView):

    def get_queryset(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        queryset = Recipe.objects.filter(comments__user=user).order_by('id').distinct('id')

        return self.filter_queryset_by_search(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_page"] = False

        return context


def approve_recipe(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied

    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.is_approved = True
    recipe.save()

    return redirect(request.META.get('HTTP_REFERER', '/dashboard'))
