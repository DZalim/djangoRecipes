from django.contrib.auth import get_user_model
from django.db import models

from djangoRecipes.common.utils import TimeStampMixin
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()


class Comment(TimeStampMixin):
    class Meta:
        indexes = [
            models.Index(fields=['updated_at']),
        ]
        ordering = ['-updated_at']

    description = models.TextField(max_length=300)

    to_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comments")

    def comment_info(self):
        return f"Comment added from {self.user} to recipe {self.to_recipe.recipe_name}"


class Like(models.Model):
    to_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="likes")

    def like_info(self):
        return f"User '{self.user}' has liked recipe - '{self.to_recipe.recipe_name}'"
