from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoRecipes.recipes'

    def ready(self):
        import djangoRecipes.recipes.signals
