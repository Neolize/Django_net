import logging

from applications.abstract_activities.models import AbstractPost


LOGGER = logging.getLogger('main_logger')


def delete_post(post: AbstractPost) -> None:
    try:
        post.delete()
    except Exception as exc:
        LOGGER.error(exc)
