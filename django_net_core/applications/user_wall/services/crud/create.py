import logging

from django.db.utils import DataError

from applications.user_wall import models
from applications.user_wall.services.crud import crud_utils


LOGGER = logging.getLogger('main_logger')


def create_user_post_from_form_data(data: dict, user_pk: int) -> bool:
    is_published = not data.get('draft')
    return _create_user_post(
        title=data.get('title'),
        content=data.get('content'),
        tags=data.get('tags'),
        user_pk=user_pk,
        is_published=is_published,
    )


def _create_user_post(
        title: str,
        content: str,
        user_pk: int,
        is_published: bool,
        tags: str,
) -> bool:

    slug = crud_utils.return_unique_slug(str_for_slug=title, model=models.UserPost)
    tags = _create_tags_from_list(
        crud_utils.form_tag_list(tags)
    )
    try:
        new_post = models.UserPost.objects.create(
            title=title,
            content=content,
            slug=slug,
            is_published=is_published,
            author_id=user_pk,
        )
        _add_tags_to_user_post(tags=tags, post=new_post)
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created


def _create_new_tag(new_tag: str) -> models.Tag | bool:
    slug = crud_utils.return_unique_slug(str_for_slug=new_tag, model=models.Tag)
    try:
        created_tag = models.Tag.objects.create(title=new_tag.lower(), slug=slug)
    except DataError as exc:
        LOGGER.error(exc)
        created_tag = False

    return created_tag


def _create_tags_from_list(tag_list: list[str]) -> list[models.Tag]:
    tags = []
    for tag in tag_list:
        new_tag = _create_new_tag(tag)
        if not new_tag:
            raise Exception('Error occurred during creating a new post')
        tags.append(new_tag)

    return tags


def _add_tags_to_user_post(tags: list[models.Tag], post: models.UserPost) -> None:
    for tag in tags:
        post.tags.add(tag)
