import logging

from django.db.models import QuerySet, Count
from django.core.exceptions import ObjectDoesNotExist

from applications.groups import models
from applications.user_profiles.models import CustomUser


LOGGER = logging.getLogger('main_logger')


def get_group_by_slug(group_slug: str) -> models.Group | bool:
    try:
        group = models.Group.objects.select_related('creator').get(slug__iexact=group_slug)
    except ObjectDoesNotExist as exc:
        LOGGER.warning(f'Group with slug - {group_slug} does not exist. {exc}')
        group = False

    return group


def does_user_have_group(user: CustomUser) -> bool:
    return user.user_groups.exists()


def is_user_allowed_to_create_group(user: CustomUser) -> bool:
    return user.user_groups.count() < 5  # user can't own more than 5 groups


def get_related_group_posts(group: models.Group) -> QuerySet[models.GroupPost]:
    return (
        group.group_posts.filter(is_published=True).order_by('-publication_date').
        select_related('author').prefetch_related('tags').
        annotate(comments_number=Count('comments'))
    )

