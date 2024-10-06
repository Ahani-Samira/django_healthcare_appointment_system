# tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import phone_number_validator
from .models import CustomUser, Doctor, Patient

class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user_attributes = {
            'phone_number': '09123456789',
            'password': 'securepassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'Male',
        }

    def test_valid_phone_number(self):
        user = CustomUser(**self.user_attributes)
        try:
            phone_number_validator(user.phone_number)
        except ValidationError:
            self.fail("phone_number_validator raised ValidationError unexpectedly!")

    def test_invalid_phone_number_length(self):
        self.user_attributes.pop('phone_number')
        user = CustomUser(phone_number='0912345678', **self.user_attributes)
        with self.assertRaises(ValidationError) as cm:
            phone_number_validator(user.phone_number)
        self.assertEqual(cm.exception.code, 'length')

    def test_invalid_phone_number_digits(self):
        self.user_attributes.pop('phone_number')
        user = CustomUser(phone_number='0912345678a', **self.user_attributes)
        with self.assertRaises(ValidationError) as cm:
            phone_number_validator(user.phone_number)
        self.assertEqual(cm.exception.code, 'digits')

    def test_invalid_phone_number_prefix(self):
        self.user_attributes.pop('phone_number')
        user = CustomUser(phone_number='12345678901', **self.user_attributes)
        with self.assertRaises(ValidationError) as cm:
            phone_number_validator(user.phone_number)
        self.assertEqual(cm.exception.code, 'prefix')

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_attributes)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

    def test_create_doctor(self):
        self.user_attributes['is_doctor'] = True
        user = CustomUser.objects.create_user(**self.user_attributes)
        self.assertIsNotNone(user.id)
        doctor = Doctor.objects.get(user=user)
        self.assertIsNotNone(doctor)

    def test_create_patient(self):
        user = CustomUser.objects.create_user(**self.user_attributes)
        patient = Patient.objects.get(user=user)
        self.assertIsNotNone(patient)

    def test_slug_is_created(self):
        user = CustomUser.objects.create_user(**self.user_attributes)
        self.assertTrue(user.slug)
        self.assertIn('1-john-doe', user.slug)

    def test_slug_update_on_save(self):
        user = CustomUser.objects.create_user(**self.user_attributes)
        original_slug = user.slug
        user.first_name = 'Jane'
        user.save()
        self.assertNotEqual(original_slug, user.slug)
        self.assertIn('1-jane-doe', user.slug)

class UserSignalTests(TestCase):

    def test_create_doctor_profile_signal(self):
        user = CustomUser.objects.create_user(
            phone_number='09123456788',
            password='securepassword',
            first_name='Alice',
            last_name='Wonderland',
            gender = 'Fmale',
            is_doctor=True
        )
        doctor = Doctor.objects.get(user=user)
        self.assertIsNotNone(doctor)

    def test_create_patient_profile_signal(self):
        user = CustomUser.objects.create_user(
            phone_number='09123456789',
            password='securepassword',
            first_name='Bob',
            last_name='Builder',
            gender = 'Male',
            is_doctor=False
        )
        patient = Patient.objects.get(user=user)
        self.assertIsNotNone(patient)

    def test_save_doctor_profile_signal(self):
        user = CustomUser.objects.create_user(
            phone_number='09123456790',
            password='securepassword',
            first_name='Dr. Who',
            last_name='Time',
            gender='Male',
            is_doctor=True
        )
        user.first_name = 'Dr. Time'
        user.save()
        self.assertIsNotNone(user.doctor)

    def test_save_patient_profile_signal(self):
        user = CustomUser.objects.create_user(
            phone_number='09123456791',
            password='securepassword',
            first_name='Patient',
            last_name='Zero',
            gender='Male',
            is_doctor=False
        )
        user.first_name = 'Changed'
        user.save()
        self.assertIsNotNone(user.patient)
