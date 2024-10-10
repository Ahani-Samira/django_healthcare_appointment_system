import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from .validators import phone_number_validator


class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    UNSET = 'U', _('Unset')


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, gender=Gender.UNSET,
                    first_name=None, last_name=None, date_of_birth=None,
                    **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be provided')
        if not (password and first_name and last_name):
            raise ValueError('Password, first name, and last name must be provided')

        extra_fields.setdefault('is_doctor', False)

        user = self.model(
            phone_number=phone_number,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True, unique=True,
        default=uuid.uuid4, editable=False,
        verbose_name=_("ID")
    )
    gender = models.CharField(
        max_length=1, choices=Gender.choices,
        default=Gender.UNSET, verbose_name=_("Gender")
    )
    slug = models.SlugField(null=True, blank=True, editable=False, verbose_name=_("Slug"))
    phone_number = models.CharField(
        max_length=11, validators=[phone_number_validator],
        unique=True, verbose_name=_("Phone Number")
    )
    first_name = models.CharField(max_length=30, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=30, verbose_name=_("Last Name"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Date of Birth"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_doctor = models.BooleanField(default=False, null=True, blank=True, verbose_name=_("Is Doctor"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{str(self.id)[:8]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    specialty = models.CharField(max_length=100, verbose_name=_("Specialty"))
    medical_code = models.CharField(max_length=50, unique=True, verbose_name=_("Medical Code"))
    photo = models.ImageField(upload_to='doctor_photos/', verbose_name=_("Photo"))

    def save(self, *args, **kwargs):
        self.photo.name = f"doctor_{self.medical_code}.png"
        self.user.slug = slugify(f"{self.user.first_name}-{self.user.last_name}-{self.medical_code}")
        super().save(*args, **kwargs)

    def __str__(self):
        return gettext(f"Dr.{self.user.first_name} {self.user.last_name} ({self.specialty})")

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")


class Patient(models.Model):
    class InsuranceType(models.TextChoices):
        HEALTH = 'H', _('Health')
        SOCIAL_SECURITY = 'S', _('Social Security')
        ARMED_FORCES = 'A', _('Armed Forces')
        NOT_INSURED = 'N', _('Not Insured')

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    insurance_type = models.CharField(
        max_length=1, choices=InsuranceType.choices,
        default=InsuranceType.NOT_INSURED,
        verbose_name=_("Insurance Type")
    )
    photo = models.ImageField(
        upload_to='user_photos/', null=True,
        blank=True, verbose_name=_("Photo")
    )

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo.name = f"patient_{str(self.user.id)[:10]}.png"

        self.user.slug = slugify(f"{str(self.id)[:8]}-{self.user.first_name}-{self.user.last_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
