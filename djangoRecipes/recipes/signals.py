from django.db.models.signals import pre_delete
from django.dispatch import receiver

from djangoRecipes.recipes.models import Recipe


@receiver(pre_delete, sender=Recipe)
def delete_recipe_photos(sender, instance, **kwargs):
    photos = instance.photos.all()

    for photo in photos:
        photo.delete_photo_from_cloudinary()
