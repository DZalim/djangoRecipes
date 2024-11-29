from django.db.models.signals import pre_delete
from django.dispatch import receiver

from djangoRecipes.categories.models import Category


@receiver(pre_delete, sender=Category)
def delete_category_photos(sender, instance, **kwargs):
    recipes = instance.recipes.all()

    for recipe in recipes:
        photos = recipe.photos.all()
        for photo in photos:
            photo.delete_photo_from_cloudinary()
