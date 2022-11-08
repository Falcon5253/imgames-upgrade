from django.apps import AppConfig


class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rooms'
    verbose_name = 'Комнаты и ходы'

    def ready(self):
        import apps.rooms.signals
