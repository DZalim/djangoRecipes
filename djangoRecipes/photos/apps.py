from django.apps import AppConfig


class PhotosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoRecipes.photos'

    def ready(self):
        import djangoRecipes.photos.signals
