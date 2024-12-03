from django.contrib.auth import get_user_model
from django.db import models

from djangoRecipes.common.utils import TimeStampMixin

UserModel = get_user_model()


class Category(TimeStampMixin):
    category_name = models.CharField(
        max_length=30,
        unique=True,
        error_messages={
            "unique": "Тhis category already exists!",
        },
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
