from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify as django_slugify


# def slugify(str_for_slugify: str) -> str:
#     alphabet = {
#         'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
#         'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
#         'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'i', 'ь': '',
#         'э': 'e', 'ю': 'yu', 'я': 'ya',
#     }
#     return django_slugify(''.join(alphabet.get(letter, letter) for letter in str_for_slugify.lower()))
#
#
# def is_unique_slug(model: models, slug: str) -> bool:
#     if model.objects.filter(slug__iexact=slug).exists():
#         return False
#     return True


class CustomUser(AbstractUser):
    """Custom user model"""
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('not specified', 'not specified')
    )
    middle_name = models.CharField(max_length=50, blank=True)
    first_login = models.DateTimeField(null=True)
    avatar = models.ImageField(upload_to='user/avatar/%Y/%m/%d/', blank=True, null=True)
    gender = models.CharField(max_length=13, choices=GENDER, default='not specified')


class UserPersonalData(models.Model):
    """Additional information about user"""
    phone = models.CharField(max_length=18)
    birthday = models.DateField(blank=True, null=True)
    info_about_user = models.TextField(max_length=1000, blank=True)
    address = models.CharField(max_length=150, blank=True)
    work = models.CharField(max_length=150, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_data')


class Hobby(models.Model):
    """User's hobby model"""
    title = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="hobbies")


# class Group(models.Model):
#     """User's group"""
#     title = models.CharField(max_length=100, db_index=True)
#     description = models.TextField(max_length=1000, blank=True)
#     logo = models.ImageField(upload_to='group/logo/%Y/%m/%d/', blank=True, null=True)
#     creation_date = models.DateField(auto_now_add=True)
#     slug = models.SlugField(max_length=125, blank=True, unique=True)
#     creator = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_groups'
#     )
#
#
# class Tag(models.Model):
#     """Tag model for posts"""
#     title = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=50, blank=True, unique=True)
#
#
# class Post(models.Model):
#     """User's post model"""
#     title = models.CharField(max_length=150, db_index=True)
#     content = models.TextField()
#     publication_date = models.DateTimeField(auto_now_add=True)
#     last_edit = models.DateTimeField(auto_now=True)
#     view_counts = models.PositiveIntegerField()
#     slug = models.SlugField(max_length=175, blank=True, unique=True)
#     is_published = models.BooleanField(default=True)
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_posts'
#     )
#     tags = models.ManyToManyField('Tag', blank=True, related_name="posts")
