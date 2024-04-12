import logging

from applications.user_wall.models import UserPost
from applications.groups.models import GroupPost
from applications.user_wall.services.crud.read import get_tag_by_title


LOGGER = logging.getLogger('main_logger')


def delete_tag_from_post(tag_title: str, post: UserPost | GroupPost) -> None:
    tag = get_tag_by_title(tag_title)
    try:
        post.tags.remove(tag)
    except Exception as exc:
        LOGGER.error(exc)
