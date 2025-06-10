from django.apps import AppConfig


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'
    # for Persian localization app name in the admin panel
    # verbose_name = 'بلاگ'
