from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from djangoRecipes.categories.models import Category
from djangoRecipes.common.utils import TimeStampMixin
from djangoRecipes.recipes.choices import RecipeDifficultyLevelChoices
from djangoRecipes.recipes.validators import SemicolonValidator

UserModel = get_user_model()


class Recipe(TimeStampMixin):
    class Meta:
        indexes = [
            models.Index(fields=['updated_at']),
        ]
        ordering = ['-updated_at']

    recipe_name = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            "unique": "A recipe with the same name already exists. "
                      "Please choose another name for your recipe!",
        },
    )
    difficulty_level = models.CharField(max_length=10, choices=RecipeDifficultyLevelChoices.choices)
    portions = models.SmallIntegerField(validators=[MinValueValidator(1)], )
    preparing_time = models.SmallIntegerField(validators=[MinValueValidator(1)], )  # should be in minutes
    cooking_time = models.SmallIntegerField(validators=[MinValueValidator(1)], )  # should be in minutes
    ingredients = models.TextField(validators=[SemicolonValidator()])  # must be entered with a semicolon(;)
    description = models.TextField(validators=[MinLengthValidator(50)])
    is_approved = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="recipes")

    def __str__(self):
        return self.recipe_name
