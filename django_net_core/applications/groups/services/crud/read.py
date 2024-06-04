import logging

from django.db.models import QuerySet, Count, Prefetch
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


def get_related_group_posts(
        group: models.Group,
        posts_to_show: str,
        owner: bool = False
) -> QuerySet[models.GroupPost]:
    """If owner of the group visits this page with the parameter 'posts_to_show' set,
    the function will return posts depending on the value of this variable.
    Without this parameter set, an owner will get all posts regardless of flag 'is_published',
    but all visitor will get posts with flag 'is_published=True'."""
    if posts_to_show and owner:
        return _fetch_chosen_group_posts(posts_to_show, group)

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


def _fetch_chosen_group_posts(posts_to_show: str, group: models.Group) -> QuerySet[models.GroupPost]:
    """Return published or unpublished group posts depending on 'posts_to_show' parameter."""
    if posts_to_show.lower() == 'published':
        return (
            group.group_posts.filter(is_published=True).order_by('-publication_date').
            select_related('author').prefetch_related('tags').
            annotate(comments_number=Count('comments'))
        )
    elif posts_to_show.lower() == 'unpublished':
        return (
            group.group_posts.filter(is_published=False).order_by('-publication_date').
            select_related('author').prefetch_related('tags').
            annotate(comments_number=Count('comments'))
        )
    else:
        return (
            group.group_posts.all().order_by('-publication_date').
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
            'member__group_comments',
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


def get_group_comment_by_pk(comment_pk: int) -> models.GroupComment | bool:
    try:
        comment = models.GroupComment.objects.get(pk=comment_pk)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'Group comment with pk - {comment_pk} does not exist. {exc}')
        comment = False

    return comment


def get_group_post_by_pk(post_pk: int) -> models.GroupPost | bool:
    try:
        post = models.GroupPost.objects.get(pk=post_pk)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'Group post with pk - {post_pk} does not exist. {exc}')
        post = False

    return post


def get_all_groups() -> QuerySet[models.Group]:
    """Return all groups."""
    return (
        models.Group.objects.all().order_by('pk').
        prefetch_related(
            'group_members',
            'group_posts',
        ).
        annotate(
            comments=Count('group_posts__comments')
        )
    )


def fetch_groups_by_titles(user_input: str) -> QuerySet[models.Group]:
    """Return groups selected by titles."""
    return (
        models.Group.objects.filter(title__icontains=user_input).
        perfetch_related(
            'group_members',
            'group_posts',
        )
    )
