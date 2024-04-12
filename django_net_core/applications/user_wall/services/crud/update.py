import logging
import pytz
from datetime import datetime

from django.db.models import QuerySet

from django_net_core.settings import TIME_ZONE
from applications.user_wall import models
from applications.user_wall.services.crud import crud_utils, create
from applications.user_wall.services.crud.delete import delete_tag_from_user_post


LOGGER = logging.getLogger('main_logger')


def update_user_post(data: dict, post: models.UserPost) -> bool:
    is_published = not data.get('draft')
    new_title = data.get('title')
    new_tags = crud_utils.form_tag_list(data.get('tags'))
    old_tags = [tag.title for tag in post.tags.all()]

    if not is_user_post_changed(
        post=post,
        new_title=new_title,
        new_content=data.get('content'),
        new_tags=crud_utils.form_tag_list(data.get('tags')),
        old_tags=[tag.title for tag in post.tags.all()],
        is_published=is_published,
    ):
        return True

    if new_tag_list := _return_new_tag_list(
        new_tags=new_tags,
        old_tags=old_tags,
        post=post,
    ):
        tags = create.return_tag_objects_from_list(new_tag_list)
    else:
        tags = []

    if post.title != new_title:
        slug = crud_utils.return_unique_slug(str_for_slug=new_title, model=models.UserPost)
    else:
        slug = post.slug

    dt = datetime.now()
    time_zone = pytz.timezone(TIME_ZONE)

    try:
        post.title = new_title
        post.content = data.get('content')
        post.slug = slug
        post.is_published = is_published
        post.last_edit = time_zone.localize(dt)

        create.add_tags_to_post(tags=tags, post=post)
        post.save()
        is_edited = True
    except Exception as exc:
        LOGGER.error(exc)
        is_edited = False

    return is_edited


def _return_new_tag_list(new_tags: list[str], old_tags: list[str], post: models.UserPost) -> list[str]:
    """
    If a set of tags was changed, the function would return a new set of tag as a list.
    Otherwise, return an old tag list.
    """
    new_tags_set = set(new_tags)
    old_tags_set = set(old_tags)
    added_tags_list = list(new_tags_set.difference(old_tags_set))

    if not added_tags_list:
        if len(old_tags) > len(new_tags):
            discarded_tags = list(old_tags_set.difference(new_tags_set))
            for tag in discarded_tags:
                delete_tag_from_user_post(tag_title=tag, post=post)
        return new_tags

    return added_tags_list


def update_user_posts_view_count(
        user_pk: int,
        visitor_pk: int,
        posts: QuerySet[models.UserPost]
) -> None:
    if visitor_pk == user_pk:
        return None

    for post in posts:
        if visitor_pk not in post.user_list:
            # increase counter when the appropriate page is opened
            post.view_counts += 1
            post.user_list.append(visitor_pk)
            post.save()


def is_user_post_changed(
        post: models.UserPost,
        new_title: str,
        new_content: str,
        new_tags: list[str | None],
        old_tags: list[str | None],
        is_published: bool,
) -> bool:
    """Check for changes in the post"""
    if ((post.title != new_title) or (post.content != new_content) or
            (post.is_published != is_published) or (set(new_tags) != set(old_tags))):
        return True

    return False
