from django.db import models
from django.conf import settings


class Group(models.Model):
    """User's group"""
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=1000, blank=True)
    logo = models.ImageField(upload_to='group/logo/%Y/%m/%d/', blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=125, blank=True, unique=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_groups'
    )
