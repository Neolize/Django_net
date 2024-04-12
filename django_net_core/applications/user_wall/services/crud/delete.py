import logging

from applications.user_wall.models import UserPost
from applications.user_wall.services.crud.read import get_tag_by_title


LOGGER = logging.getLogger('main_logger')


def delete_user_post(user_post: UserPost) -> None:
    try:
        user_post.delete()
    except Exception as exc:
        LOGGER.error(exc)


def delete_tag_from_user_post(tag_title: str, post: UserPost) -> None:
    tag = get_tag_by_title(tag_title)
    try:
        post.tags.remove(tag)
    except Exception as exc:
        LOGGER.error(exc)
