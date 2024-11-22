from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from djangoRecipes.accounts.models import Profile
from djangoRecipes.common.mixins import ReadOnlyMixin

UserModel = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class UserForm(ReadOnlyMixin, forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["username", "email"]

    readonly_fields = ["username", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_form = UserForm(instance=self.instance.user)

        for name, field in user_form.fields.items():
            self.fields[name] = field

        for name, value in user_form.initial.items():
            self.initial[name] = value
