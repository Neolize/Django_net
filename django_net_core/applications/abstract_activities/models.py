from django.db import models


class AbstractPost(models.Model):
    """Abstract Post model"""
    title = models.CharField(max_length=150, db_index=True)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    view_counts = models.PositiveIntegerField()
    slug = models.SlugField(max_length=175, blank=True, unique=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AbstractComment(models.Model):
    """Abstract Comment model"""
    content = models.TextField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
