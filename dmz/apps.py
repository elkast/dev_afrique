from django.apps import AppConfig


class DmzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dmz'
    verbose_name = 'DMZ — Sécurité'

    def ready(self):
        import dmz.signals  # noqa: F401
