from django.apps import AppConfig


class ClassInteractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'class_interaction'
    verbose_name = '课堂互动'

    def ready(self):
        import class_interaction.signals  # noqa
