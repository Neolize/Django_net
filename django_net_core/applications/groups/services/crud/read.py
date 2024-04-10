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


def fetch_all_group_followers(group: models.Group) -> QuerySet[models.GroupMember]:
    return (
        group.group_members.all().select_related(
            'member',
            'member__personal_data',
            'member__contacts',
        ).
        prefetch_related(
            'member__followers',
            'member__user_comments',
            'member__user_groups',
        )
    )


def fetch_group_post(group_post_slug: str) -> models.GroupPost | bool:
    try:
        group_post = models.GroupPost.objects.get(slug=group_post_slug)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'Group post with slug - {group_post_slug} does not exist. {exc}')
        group_post = False

    return group_post
