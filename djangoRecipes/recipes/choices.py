from django.db import models


class RecipeDifficultyLevelChoices(models.TextChoices):
    EASY = "Easy", "Easy"
    MEDIUM = "Medium", "Medium"
    HARD = "Hard", "Hard"
