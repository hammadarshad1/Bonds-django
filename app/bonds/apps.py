from django.apps import AppConfig


class BondsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bonds'

    def ready(self) -> None:
        import bonds.signals
