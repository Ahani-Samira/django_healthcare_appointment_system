from django.contrib import admin
from .models import Clinic, Availability, Appointment


admin.site.register(Clinic)
admin.site.register(Availability)
admin.site.register(Appointment)
