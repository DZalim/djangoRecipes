from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoRecipes.accounts'

    def ready(self):
        import djangoRecipes.accounts.signals