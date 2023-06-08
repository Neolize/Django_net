import logging

from django.db.models import QuerySet

from applications.user_wall import models


LOGGER = logging.getLogger('main_logger')


def get_user_posts(user_pk) -> QuerySet[models.UserPost]:
    # return models.UserPost.objects.filter(author_id=user_pk).prefetch_related('tags')
    return models.UserPost.objects.filter(author_id=user_pk).order_by('-publication_date')


def get_user_post(slug: str) -> models.UserPost | bool:
    try:
        post = models.UserPost.objects.filter(slug=slug).prefetch_related('tags')[0]
    except IndexError as exc:
        LOGGER.warning(f'User\'s post with slug - {slug} does not exist. {exc}')
        post = False

    return post

#  posts = models.UserPost.objects.filter(author_id=6, is_published=True).
#  values('title', 'content', 'publication_date', 'last_edit', 'view_counts', 'tags__title')

# def get_user_posts(user_pk) -> QuerySet[models.UserPost]:
#     values = (
#         'title',
#         'content',
#         'publication_date'
#         'last_edit',
#         'view_counts',
#     )
#     return models.UserPost.objects.filter(author_id=user_pk, is_published=True).values(*values)
