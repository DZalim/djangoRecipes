from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from djangoRecipes.accounts.forms import AppUserCreationForm

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
