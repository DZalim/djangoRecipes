from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from djangoRecipes.accounts.forms import AppUserChangeForm, AppUserCreationForm
from djangoRecipes.accounts.models import Profile

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    form = AppUserChangeForm
    add_form = AppUserCreationForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    list_display = ["username", "email", "is_active", "is_staff", "is_superuser", "last_login"]
    search_fields = ["username", "email", "is_active", "is_staff", "is_superuser"]
    list_filter = ["is_active", "is_staff", "is_superuser", "last_login"]
    fieldsets = (
        ("Credentials", {
            "fields": ("username", "email", "password", "last_login")
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_superuser", 'groups', 'user_permissions')
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
    )
