from django.db import models
from django.conf import settings
from django.utils.text import slugify as django_slugify

from mptt.models import MPTTModel, TreeForeignKey

from applications.abstract_activities import models as abstract_models


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

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.title


class UserPost(abstract_models.AbstractPost):
    """User's post model"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_posts'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='user_posts')

    class Meta:
        db_table = 'post'

    def __str__(self):
        return f'{self.title} - {self.author}'


class UserComment(abstract_models.AbstractComment, MPTTModel):
    """User's comment model"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_comments'
    )
    post = models.ForeignKey('UserPost', on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    class MPTTMeta:
        """Sorting by nesting"""
        order_insertion_by = ('creation_date', )

    class Meta:
        db_table = 'user_comment'

    def __str__(self):
        return f'{self.author} - {self.post}'
