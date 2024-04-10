import logging

from applications.user_wall.models import UserPost


LOGGER = logging.getLogger('main_logger')


def delete_user_post(user_post: UserPost) -> None:
    try:
        user_post.delete()
    except Exception as exc:
        LOGGER.error(exc)
