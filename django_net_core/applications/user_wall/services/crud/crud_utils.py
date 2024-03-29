import re
from time import time

from django.db.models.base import ModelBase
from django.utils.text import slugify as django_slugify


def return_unique_slug(str_for_slug: str, model: ModelBase) -> str:
    """Return unique slug based on gotten string"""
    slug = _slugify(str_for_slug)
    if not _is_unique_slug(model=model, slug=slug):
        slug = _generate_unique_slug(slug)

    return slug


def _is_unique_slug(model: ModelBase, slug: str) -> bool:
    if model.objects.filter(slug__iexact=slug).exists():
        return False
    return True


def _generate_unique_slug(slug: str) -> str:
    return f'{slug}-{int(time())}'


def _slugify(str_for_slugify: str) -> str:
    alphabet = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'i', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    return django_slugify(''.join(alphabet.get(letter, letter) for letter in str_for_slugify.lower()))


def form_tag_list(tags: str) -> list[str]:
    match = re.findall(r'#\s*([^,;]+)', tags)
    return match
