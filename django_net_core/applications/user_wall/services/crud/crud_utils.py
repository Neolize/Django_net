from time import time

from django.utils.text import slugify as django_slugify
from django.db.models.base import ModelBase


def is_unique_slug(model: ModelBase, slug: str) -> bool:
    if model.objects.filter(slug__iexact=slug).exists():
        return False
    return True


def generate_unique_slug(slug: str) -> str:
    return f'{slug}-{int(time())}'


def slugify(str_for_slugify: str) -> str:
    alphabet = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'i', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    return django_slugify(''.join(alphabet.get(letter, letter) for letter in str_for_slugify.lower()))
