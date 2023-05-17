from django.db import models
from django.conf import settings

from applications.abstract_activities import models as abstract_models
from applications.user_wall.models import Tag


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

    def __str__(self):
        return f'{self.title}'


class GroupPost(abstract_models.AbstractPost):
    """Group's Post model"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='group_posts'
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='group_posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='group_posts')

    def __str__(self):
        return f'{self.title}'


class GroupComment(abstract_models.AbstractComment):
    """Group's Comment model"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='group_comments'
    )
    post = models.ForeignKey('GroupPost', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.creation_date}'
