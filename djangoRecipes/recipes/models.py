from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from djangoRecipes.categories.models import Category
from djangoRecipes.common.utils import TimeStampMixin
from djangoRecipes.recipes.choices import RecipeDifficultyLevelChoices
from djangoRecipes.recipes.validators import SemicolonValidator

UserModel = get_user_model()


class Recipe(TimeStampMixin):
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

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="recipes")
