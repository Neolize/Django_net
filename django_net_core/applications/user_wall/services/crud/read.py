import logging

from django.db.models import QuerySet

from applications.user_wall import models


LOGGER = logging.getLogger('main_logger')


def get_user_posts(user_pk: int) -> QuerySet[models.UserPost]:
    return models.UserPost.objects.filter(author_id=user_pk, is_published=True)\
        .order_by('-publication_date').prefetch_related('tags')


def get_user_post(slug: str) -> models.UserPost | bool:
    try:
        post = models.UserPost.objects.filter(slug=slug).prefetch_related('tags')[0]
    except IndexError as exc:
        LOGGER.warning(f'User\'s post with slug - {slug} does not exist. {exc}')
        post = False

    return post
