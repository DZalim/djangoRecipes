from cloudinary import CloudinaryResource
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from djangoRecipes.common.utils import TimeStampMixin
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()


class BasePhoto(TimeStampMixin):
    class Meta:
        abstract = True

    photo_url = CloudinaryField("Upload a photo from your device", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if isinstance(self.photo_url, CloudinaryResource):
            self.photo_url = self.photo_url.build_url()

        super().save(*args, **kwargs)


class UsersPhoto(BasePhoto):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="profile_picture")


class RecipePhotos(BasePhoto):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="photos")
