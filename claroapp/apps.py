from django.apps import AppConfig

class ClaroappConfig(AppConfig):
    name = 'claroapp'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import claroapp.signals