from django.db.models.signals import post_delete, pre_delete, pre_save
from django.dispatch import receiver

from djangoRecipes.photos.models import RecipePhotos, UsersPhoto


@receiver(post_delete, sender=RecipePhotos)
@receiver(post_delete, sender=UsersPhoto)
def delete_recipe_photo(sender, instance, **kwargs):
    instance.delete_photo_from_cloudinary()

