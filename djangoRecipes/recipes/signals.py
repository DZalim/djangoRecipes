from django.core.mail import send_mail
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from djangoRecipes.recipes.models import Recipe
from djangoRecipes.settings import FROM_EMAIL


@receiver(pre_delete, sender=Recipe)
def delete_recipe_photos(sender, instance, **kwargs):
    photos = instance.photos.all()

    for photo in photos:
        photo.delete_photo_from_cloudinary()

@receiver(post_save, sender=Recipe)
def send_approval_email(sender, instance, created, **kwargs):
    if not created and instance.is_approved:

        user = instance.user
        send_mail(
            subject=f"Your recipe '{instance.recipe_name}' has been approved",
            message=f"Hello, {user.username},\n "
                    f"The recipe you added has already been approved. You can see it in the dashboard.\n"
                    f"Thank you for being part of ours.\n"
                    f"We expect your delicious recipes to reach a wide range of people.\n"
                    f"\n"
                    f"Best Regards,\n"
                    f"Django Recipes\n",
            from_email=FROM_EMAIL,
            recipient_list=[instance.email],  # user.email
            fail_silently=False
        )

