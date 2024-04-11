import logging

from django.db.models import QuerySet, Count
from django.core.exceptions import ObjectDoesNotExist

from applications.user_wall import models
from applications.user_profiles.models import CustomUser


LOGGER = logging.getLogger('main_logger')


def get_related_posts(user: CustomUser) -> QuerySet[models.UserPost]:
    return user.user_posts.filter(is_published=True).order_by('-publication_date').\
        prefetch_related('tags').annotate(comments_number=Count('comments'))


def get_user_post(slug: str) -> models.UserPost | bool:
    try:
        post = models.UserPost.objects.filter(slug=slug).prefetch_related('tags')[0]
    except IndexError as exc:
        LOGGER.warning(f'User\'s post with slug - {slug} does not exist. {exc}')
        post = False

    return post


def fetch_user_post(user_post_slug: str) -> models.UserPost | bool:
    try:
        user_post = models.UserPost.objects.get(slug=user_post_slug)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'User post with slug - {user_post_slug} does not exist. {exc}')
        user_post = False

    return user_post


def get_tag_by_title(tag: str) -> models.Tag | bool:
    try:
        tag = models.Tag.objects.get(title__iexact=tag)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'Tag with title - {tag} does not exist. {exc}')
        tag = False

    return tag
