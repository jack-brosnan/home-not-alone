from django.apps import AppConfig


class SecretSantaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'secret_santa'

    def ready(self):
        import secret_santa.signals