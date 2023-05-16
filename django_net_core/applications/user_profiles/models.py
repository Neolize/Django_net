from django.db import models
from django.conf import settings
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
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    gender = models.CharField(max_length=13, choices=GENDER, default='not specified')


class UserPersonalData(models.Model):
    """Additional information about user"""
    phone = models.CharField(max_length=18)
    birthday = models.DateField(blank=True, null=True)
    info_about_user = models.TextField(max_length=1000, blank=True)
    address = models.CharField(max_length=150, blank=True)
    work = models.CharField(max_length=150, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="personal_data")


class Group(models.Model):
    """User's group"""
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    logo = models.ImageField(upload_to='group/logo/%Y/%m/%d/', blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="user_groups"
    )
