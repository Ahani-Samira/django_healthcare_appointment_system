from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import Doctor, Patient
from .validators import validate_same_day, validate_minimum_duration, validate_not_past_date


class Clinic(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    address = models.CharField(max_length=300, verbose_name=_("Address"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Clinic")
        verbose_name_plural = _("Clinics")


class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name=_("Doctor"))
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name=_("Clinic"))
    start_time = models.DateTimeField(
        verbose_name=_("Start time"),
        default=timezone.now(),
        validators=[validate_not_past_date]
    )
    end_time = models.DateTimeField(verbose_name=_("End time"))
    selectable_time_list = models.JSONField(default=dict, null=True, blank=True, verbose_name=_("Selectable times"))

    class Meta:
        verbose_name = _("Availability")
        verbose_name_plural = _("Availabilities")

    def clean(self):
        super().clean()
        if self.start_time and self.end_time:
            validate_same_day(self.start_time, self.end_time)
            validate_minimum_duration(self.start_time, self.end_time, visit_time=10)

    def calculation_of_time_slots(self, visit_time=10, break_time=0):
        slots = {}
        current_time = self.start_time
        selectable = True
        while current_time < self.end_time:
            time = current_time.strftime('%H:%M')
            slots[time] = selectable
            current_time += timedelta(minutes=visit_time+break_time)
        self.selectable_time_list = slots

    def get_available_time_slots(self):
        selectable_slots = self.selectable_time_list or {}
        available_slots = [time for time, is_selectable in selectable_slots.items() if is_selectable]
        return available_slots

    def save(self, *args, **kwargs):
        self.clean()
        if not self.selectable_time_list :
            self.calculation_of_time_slots()
        super().save(*args, **kwargs)

    def __str__(self):
        date = self.start_time.date()
        start = self.start_time.strftime('%H:%M')
        end = self.end_time.strftime('%H:%M')
        return f"{self.doctor}-{date}({start}-{end})"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name=_("Patient"))
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, verbose_name=_("Availability"))
    selected_time = models.CharField(max_length=5, null=True, blank=True, verbose_name=_("Selected Time"))

    class Meta:
        unique_together = ('patient', 'availability')
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def clean(self):
        try:
            selectable_slots = self.availability.selectable_time_list or {}
            if not selectable_slots.get(self.selected_time, False):
                raise ValidationError(_("Selected time is not available."))
        except Exception:
            raise ValidationError(_("Selected time could not be verified."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        selectable_slots = self.availability.selectable_time_list
        if self.selected_time in selectable_slots:
            selectable_slots[self.selected_time] = False
            self.availability.save()

    def delete(self, *args, **kwargs):
        selectable_slots = self.availability.selectable_time_list
        if self.selected_time in selectable_slots:
            selectable_slots[self.selected_time] = True
            self.availability.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} - {self.availability.doctor}"
