from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from djangoRecipes.accounts.forms import AppUserCreationForm
from djangoRecipes.accounts.models import Profile
from djangoRecipes.common.models import Comment
from djangoRecipes.recipes.forms import CreateRecipeForm

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-view.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-view.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='djangoRecipes.accounts.authentication.EmailOrUsernameBackend')
        return response

class ProfileDetailsView(DetailView):
    model = Profile
    template_name = "accounts/profile-details-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipes"] = self.object.user.recipes.all()[:2]
        context["form"] = CreateRecipeForm()
        context["more_recipes"] = self.object.user.recipes.all().count() - 2
        unique_comments = Comment.objects.filter(user=self.request.user).order_by("to_recipe_id").distinct('to_recipe_id')
        context["unique_comments_count"] =  unique_comments.count()

        return context
