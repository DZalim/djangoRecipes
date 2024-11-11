from django.contrib.auth import get_user_model
from django.db import models

from djangoRecipes.common.models import TimeStampMixin

UserModel = get_user_model()


class Profile(TimeStampMixin):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True
    )

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name

        return "Anonymous User"
