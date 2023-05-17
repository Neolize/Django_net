from django.db import models
from django.conf import settings
from django.utils.text import slugify as django_slugify


def slugify(str_for_slugify: str) -> str:
    alphabet = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'i', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    return django_slugify(''.join(alphabet.get(letter, letter) for letter in str_for_slugify.lower()))


def is_unique_slug(model: models, slug: str) -> bool:
    if model.objects.filter(slug__iexact=slug).exists():
        return False
    return True


class Tag(models.Model):
    """Tag model for user's posts"""
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)


class Post(models.Model):
    """User's post model"""
    title = models.CharField(max_length=150, db_index=True)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    view_counts = models.PositiveIntegerField()
    slug = models.SlugField(max_length=175, blank=True, unique=True)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_posts'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name="posts")
