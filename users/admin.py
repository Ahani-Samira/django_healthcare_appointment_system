from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Doctor, Patient

admin.site.site_header = _("The management panel of the healthcare appointment system")

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = _('Doctor Information')

class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = _('Patient Information')

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (DoctorInline, PatientInline)
    list_display = (
        'first_name', 'last_name', 'phone_number',
        'is_doctor', 'is_active', 'is_staff'
    )
    search_fields = ('last_name', 'phone_number')
    readonly_fields = ('slug',)
    list_filter = ('is_active', 'is_doctor', 'is_staff')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'first_name', 'last_name', 'gender', 'date_of_birth')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_doctor', 'is_staff', 'is_superuser', 'user_permissions')
        }),
        ('Additional Info', {
            'fields': ('slug',)
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'medical_code')
    search_fields = ('user__last_name', 'medical_code', 'specialty')
    list_filter = ('specialty',)
    ordering = ('user__last_name',)

    fieldsets = (
        (None, {
            'fields': ('user', 'specialty', 'medical_code', 'photo')
        }),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'insurance_type')
    search_fields = ('user__last_name',)
    list_filter = ('insurance_type',)
    ordering = ('user__last_name',)

    fieldsets = (
        (None, {
            'fields': ('user', 'insurance_type', 'photo')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
