from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView

from djangoRecipes.accounts.forms import AppUserCreationForm, ProfileEditForm
from djangoRecipes.accounts.models import Profile
from djangoRecipes.common.models import Comment
from djangoRecipes.common.permissions import SameUserPermissions
from djangoRecipes.recipes.forms import CreateRecipeForm

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-view.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-view.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='djangoRecipes.accounts.authentication.EmailOrUsernameBackend')
        return response


class ProfileDetailsView(SameUserPermissions, DetailView):
    model = UserModel
    template_name = "accounts/profile-details-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = self.object.recipes.all()[:2]
        context["form"] = CreateRecipeForm()
        context["more_recipes"] = self.object.recipes.all().count() - 2
        unique_comments = Comment.objects.filter(user=self.object).order_by("to_recipe_id").distinct('to_recipe_id')
        context["unique_comments_count"] = unique_comments.count()

        return context


class EditProfileView(SameUserPermissions, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/update-profile-form.html"

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.kwargs['pk']})


class DeleteProfileView(SameUserPermissions, DeleteView):
    model = UserModel
    success_url = reverse_lazy("dashboard")
