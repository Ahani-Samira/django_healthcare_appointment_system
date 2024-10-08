import datetime

from datetime import timedelta, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_not_past_date(value):
    if value < datetime.now():
        raise ValidationError(_("The time cannot be in the past."))

def validate_same_day(start_time, end_time):
    if end_time.date() != start_time.date():
        raise ValidationError(_("End time must be on the same day as start time."))

def validate_minimum_duration(start_time, end_time, visit_time):
    if end_time <= start_time + timedelta(minutes=visit_time):
        raise ValidationError(_(f"End time must be at least {visit_time} minutes after start time."))
