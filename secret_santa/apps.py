from django.apps import AppConfig

class SecretSantaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'secret_santa'

    def ready(self):
        import secret_santa.signals  # Ensure signals are loaded
        from invitations.signals import invite_accepted
        print(f"Invite Accepted Signal Receivers: {invite_accepted.receivers}")  # Debug