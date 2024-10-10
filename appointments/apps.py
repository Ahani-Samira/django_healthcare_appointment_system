from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    verbose_name = _("appointments")
