import logging

from django.db.models import QuerySet

from applications.groups import models

LOGGER = logging.getLogger('main_logger')


def update_group_posts_view_count(
        group: models.Group,
        visitor_pk: int,
        posts: QuerySet[models.GroupPost]
) -> None:
    if visitor_pk == group.creator.pk:
        return None

    for post in posts:
        if visitor_pk not in post.user_list:
            # increase counter when the appropriate page is opened
            post.view_counts += 1
            post.user_list.append(visitor_pk)
            post.save()
