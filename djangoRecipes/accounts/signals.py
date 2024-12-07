from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from djangoRecipes.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance: UserModel, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=UserModel)
def delete_user_profile_picture(sender, instance, **kwargs):
    if hasattr(instance, 'profile_picture') and instance.profile_picture:
        instance.profile_picture.delete()

        instance.profile_picture.delete_photo_from_cloudinary()

