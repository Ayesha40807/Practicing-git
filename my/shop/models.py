from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=200)

    def __str__(self):
        return self.medicine_name

class doctor(models.Model):
    doctor=models.CharField(max_length=30)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.doctor}"


class Patient(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField(default=0)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, default='male', max_length=10)
    mobile = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    added_time = models.DateTimeField(auto_now_add=True, null=True)

    def total_amount_paid(self):
        # Perform reverse lookup to get all visits associated with this patient
        visits = self.visit_set.all()
        # Sum up the amounts from all visits
        total_amount = sum(visit.amount for visit in visits)
        return total_amount
    
    def __str__(self):
        return self.name  # This method returns the patient's name when the object is converted to a string

    def display_name(self):
        return self.name  # Method to display the patient's name

# models.py
# models.py
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    detail = models.TextField(null=True)
    medicine_detail = models.TextField(null=True)
    note = models.TextField(null=True)
    next_visit = models.IntegerField(default=0)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    visit_date = models.DateField(default=date.today, null=True)
    old_medicines = models.ManyToManyField(Medicine, related_name='old_visits')
    medicines = models.ManyToManyField(Medicine, related_name='visits')  # New field
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    before_eating = models.BooleanField(default=False)
    after_eating = models.BooleanField(default=False)

    def patient_email(self):
        return self.patient.email


    
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    photo = models.ImageField(upload_to='media/patient_photos', blank=True)
    

    # Provide unique related names for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
    
class Reminder(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return f'{self.title} - {self.date}'

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name
    
class PatientVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient.name}'s Visit"
    

