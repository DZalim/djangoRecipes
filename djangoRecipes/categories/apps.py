from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoRecipes.categories'

    def ready(self):
        import djangoRecipes.categories.signals
