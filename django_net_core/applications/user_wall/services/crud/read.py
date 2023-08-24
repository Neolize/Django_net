import logging

from django.db.models import QuerySet, Count

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
