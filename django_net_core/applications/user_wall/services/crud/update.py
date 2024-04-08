import logging
from datetime import datetime

from django.db.models import QuerySet

from applications.user_wall import models
from applications.user_wall.services.crud import crud_utils, create

LOGGER = logging.getLogger('main_logger')


def update_user_post(data: dict, post: models.UserPost) -> bool:
    is_published = not data.get('draft')
    new_title = data.get('title')

    if post.title != new_title:
        slug = crud_utils.return_unique_slug(str_for_slug=new_title, model=models.UserPost)
    else:
        slug = post.slug

    if new_tag_list := _return_new_tag_list(
        new_tags=crud_utils.form_tag_list(data.get('tags')),
        old_tags=[tag.title for tag in post.tags.all()]
    ):
        tags = create.create_tags_from_list(new_tag_list)
    else:
        tags = []

    try:
        post.title = new_title
        post.content = data.get('content')
        post.slug = slug
        post.is_published = is_published
        post.last_edit = datetime.now()

        create.add_tags_to_post(tags=tags, post=post)
        post.save()
        is_edited = True
    except Exception as exc:
        LOGGER.error(exc)
        is_edited = False

    return is_edited


def _return_new_tag_list(new_tags: list[str], old_tags: list[str]) -> list[str]:
    new_tag_list = []
    for new_tag in new_tags:
        if new_tag not in old_tags:
            new_tag_list.append(new_tag)

    return new_tag_list


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
