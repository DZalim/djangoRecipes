from django.contrib.auth import get_user_model
from django.db import models

from djangoRecipes.common.utils import TimeStampMixin
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()

class BasePhoto(TimeStampMixin):

    class Meta:
        abstract = True

    photo_url = models.URLField(null=True, blank=True)


class UsersPhoto(BasePhoto):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="profile_picture")


class RecipePhotos(BasePhoto):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="photos")



