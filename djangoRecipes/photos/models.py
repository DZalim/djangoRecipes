import cloudinary
import cloudinary.api
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

    @property
    def public_id(self):
        if self.photo_url:
            return self.photo_url.public_id.split('/')[-1].split('.')[0]

        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if isinstance(self.photo_url, CloudinaryResource):
            self.photo_url = self.photo_url.build_url()

        super().save(*args, **kwargs)

    def delete_photo_from_cloudinary(self):
        public_id = self.public_id

        if public_id:
            try:
                result = cloudinary.api.delete_resources([public_id])
                print(f"Photo deleted from Cloudinary: {result}")
                return result
            except cloudinary.exceptions.Error as e:
                print(f"Cloudinary error while deleting photo: {e}")
                return None

        print("No public_id found, photo not deleted.")
        return None


class UsersPhoto(BasePhoto):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="profile_picture")


class RecipePhotos(BasePhoto):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="photos")
