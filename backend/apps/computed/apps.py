from django.apps import AppConfig


class ComputedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.computed'
    verbose_name = 'Рассчитанные поля'

    def ready(self):
        import apps.computed.signals
