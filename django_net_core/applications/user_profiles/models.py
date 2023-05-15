from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model"""
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('not specified', 'not specified')
    )
    middle_name = models.CharField(max_length=50, blank=True)
    first_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=18)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=13, choices=GENDER, default='not specified')
    biography = models.TextField(blank=True, null=True)
