import logging

from applications.abstract_activities.models import AbstractPost, AbstractComment


LOGGER = logging.getLogger('main_logger')


def delete_post(post: AbstractPost) -> None:
    try:
        post.delete()
    except Exception as exc:
        LOGGER.error(exc)


def delete_comment(comment: AbstractComment) -> None:
    try:
        comment.delete()
    except Exception as exc:
        LOGGER.error(exc)
