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


def get_related_group_posts(group: models.Group, owner: bool = False) -> QuerySet[models.GroupPost]:
    """If owner of the group visits this page, it'll be shown all posts regardless of flag 'is_published'"""
    if owner:
        return (
            group.group_posts.all().order_by('-publication_date').
            select_related('author').prefetch_related('tags').
            annotate(comments_number=Count('comments'))
        )
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


def get_group_post_for_editing(group_post_slug: str) -> models.GroupPost | bool:
    try:
        group_post = models.GroupPost.objects.filter(slug=group_post_slug).prefetch_related('tags')[0]
    except IndexError as exc:
        LOGGER.warning(f'Group post with slug - {group_post_slug} does not exist. {exc}')
        group_post = False

    return group_post


# def get_group_posts_number_from_group(group: models.Group, owner: bool) -> int:
#     """If a group author visits the group page, the function will return the number of all posts
#      regardless of flag 'is_published'"""
#     try:
#         if owner:
#             posts_number = group.group_posts.all().count()
#         else:
#             posts_number = group.group_posts.filter(is_published=True).count()
#     except Exception as exc:
#         LOGGER.error(exc)
#         posts_number = 0
#
#     return posts_number


def get_published_group_posts_number(group: models.Group) -> int:
    """The function returns the number of published posts."""
    try:
        posts_number = group.group_posts.filter(is_published=True).count()
    except Exception as exc:
        LOGGER.error(exc)
        posts_number = 0

    return posts_number


def get_all_group_posts_number(group: models.Group) -> int:
    """The function returns the number of all posts."""
    try:
        posts_number = group.group_posts.all().count()
    except Exception as exc:
        LOGGER.error(exc)
        posts_number = 0

    return posts_number


def get_group_members_number_from_group(group: models.Group) -> int:
    try:
        members = group.group_members.count()
    except Exception as exc:
        LOGGER.error(exc)
        members = 0

    return members
