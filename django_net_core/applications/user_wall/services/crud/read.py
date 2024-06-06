import logging

from django.db.models import QuerySet, Count, Q, Prefetch
from django.core.exceptions import ObjectDoesNotExist

from applications.user_wall import models
from applications.user_profiles.models import CustomUser


LOGGER = logging.getLogger('main_logger')


def get_related_posts(
        user: CustomUser,
        posts_to_show: str,
        owner: bool = False
) -> QuerySet[models.UserPost]:
    """If owners visit their page with the parameter 'posts_to_show' set,
    the function will return posts depending on the value this variable.
    Without this parameter set, owners will get all posts regardless of flag 'is_published',
    but all visitor will get posts with flag 'is_published=True'."""
    if posts_to_show and owner:
        return _fetch_chosen_posts(posts_to_show, user)

    if owner:
        return user.user_posts.all().order_by('-publication_date'). \
            prefetch_related('tags').annotate(comments_number=Count('comments'))

    return user.user_posts.filter(is_published=True).order_by('-publication_date').\
        prefetch_related('tags').annotate(comments_number=Count('comments'))


def _fetch_chosen_posts(posts_to_show: str, user: CustomUser) -> QuerySet[models.UserPost]:
    """Return published or unpublished posts depending on 'posts_to_show' parameter."""
    if posts_to_show.lower() == 'published':
        return user.user_posts.filter(is_published=True).order_by('-publication_date'). \
            prefetch_related('tags').annotate(comments_number=Count('comments'))

    elif posts_to_show.lower() == 'unpublished':
        return user.user_posts.filter(is_published=False).order_by('-publication_date'). \
            prefetch_related('tags').annotate(comments_number=Count('comments'))

    else:
        return user.user_posts.all().order_by('-publication_date'). \
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


def get_user_comment_by_pk(comment_pk: int) -> models.UserComment | bool:
    try:
        comment = models.UserComment.objects.get(pk=comment_pk)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'User comment with pk - {comment_pk} does not exist. {exc}')
        comment = False

    return comment


def get_user_post_by_pk(post_pk: int) -> models.UserPost | bool:
    try:
        post = models.UserPost.objects.get(pk=post_pk)
    except ObjectDoesNotExist as exc:
        LOGGER.error(f'User post with pk - {post_pk} does not exist. {exc}')
        post = False

    return post


def get_all_posts_from_all_users() -> QuerySet[models.UserPost] | list:
    """Return all posts from all users."""
    try:
        posts = (
            models.UserPost.objects.all().
            order_by('-publication_date').
            select_related('author').
            prefetch_related(
                'tags',
                Prefetch(
                    'comments',
                    models.UserComment.objects.filter(
                        parent_id__isnull=True, is_published=True
                    ).select_related('author').prefetch_related(
                        Prefetch(
                            'children',
                            models.UserComment.objects.filter(is_published=True).select_related('author'),
                            'children_comments'
                        )
                    ),
                    'post_comments'
                ),
            ).
            annotate(comments_number=Count('comments'))
        )
    except Exception as exc:
        LOGGER.error(exc)
        posts = []

    return posts


def select_posts_from_all_users_by_user_input(user_input: str) -> QuerySet[models.UserPost] | list:
    """Return all posts from all users selected by title, content or slug."""
    try:
        posts = (
            models.UserPost.objects.filter(
                Q(title__icontains=user_input) |
                Q(content__icontains=user_input) |
                Q(slug__icontains=user_input)
            ).order_by('-publication_date').
            select_related('author').
            prefetch_related(
                'tags',
                Prefetch(
                    'comments',
                    models.UserComment.objects.filter(
                        parent_id__isnull=True, is_published=True
                    ).select_related('author').prefetch_related(
                        Prefetch(
                            'children',
                            models.UserComment.objects.filter(is_published=True).select_related('author'),
                            'children_comments'
                        )
                    ),
                    'post_comments'
                ),
            ).
            annotate(comments_number=Count('comments'))
        )
    except Exception as exc:
        LOGGER.error(exc)
        posts = []

    return posts
