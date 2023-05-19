from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('not specified', 'not specified')
)


class CustomUser(AbstractUser):
    """Custom user model"""
    middle_name = models.CharField(max_length=50, blank=True)
    first_login = models.DateTimeField(null=True)
    avatar = models.ImageField(upload_to='user/avatar/%Y/%m/%d/', blank=True, null=True)
    gender = models.CharField(max_length=13, choices=GENDER_CHOICES, default='not specified')

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        name = self.username or self.first_name
        return name


class UserPersonalData(models.Model):
    """Additional information about user"""
    phone = models.CharField(max_length=18)
    birthday = models.DateField(blank=True, null=True)
    info_about_user = models.TextField(max_length=1000, blank=True)
    address = models.CharField(max_length=150, blank=True)
    work = models.CharField(max_length=150, blank=True)
    town = models.CharField(max_length=60, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_data')

    class Meta:
        verbose_name = 'Users\' personal data'
        verbose_name_plural = 'Users\' personal data'
        db_table = 'user_personal_data'

    def __str__(self):
        return self.user


class Hobby(models.Model):
    """User's hobby model"""
    title = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='hobbies')

    class Meta:
        verbose_name = 'Hobbies'
        verbose_name_plural = 'Hobbies'
        db_table = 'hobby'

    def __str__(self):
        return self.title


class Follower(models.Model):
    """User's follower model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        db_table = 'follower'

    def __str__(self):
        return f'{self.user} - {self.follower}'
