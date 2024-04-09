import logging

from django.db.models.base import ModelBase


LOGGER = logging.getLogger('main_logger')


def create_comment(
        content: str,
        author_id: int,
        post_id: int,
        parent_id: int | None,
        model: ModelBase,
) -> bool:
    try:
        model.objects.create(
            content=content,
            author_id=author_id,
            post_id=post_id,
            parent_id=parent_id
        )
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created
