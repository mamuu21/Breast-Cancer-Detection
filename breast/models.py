from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    is_radiologist = models.BooleanField(default=False)


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        (True, 'Cancer'),
        (False, 'Normal'),
    ]
    patient_id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    image = models.FileField(upload_to='images/')
    status = models.BooleanField(choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=True, blank=True)
    
    def __str__(self) -> str:
        return self.patient_id
   
class RadiologistComment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    radiologist = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.patient.patient_id
    