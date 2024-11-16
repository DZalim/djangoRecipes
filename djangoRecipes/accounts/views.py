from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from djangoRecipes.accounts.forms import AppUserCreationForm
from djangoRecipes.accounts.models import Profile

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

        return context
