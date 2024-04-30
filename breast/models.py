from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    is_radiologist = models.BooleanField(default=False)
    objects = CustomUserManager()


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
    
    def __str__(self) -> str:
        return self.patient_id
    
    # TODO : Integrae with django authentication and permissions (LOGIN, LOGOUT, PERMISSIONS)
 
    