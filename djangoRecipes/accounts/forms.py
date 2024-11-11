from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from djangoRecipes.common.mixins import PlaceholderMixin

UserModel = get_user_model()

class AppUserCreationForm(PlaceholderMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ("username", "email",)

class AppUserChangeForm(PlaceholderMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
