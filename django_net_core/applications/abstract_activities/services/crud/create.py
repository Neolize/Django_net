import logging

from django.db.models.base import ModelBase

from applications.abstract_activities.services.utils import get_parent_comment
from applications.user_profiles.models import CustomUser
from applications.groups.forms import GroupCommentForm
from applications.user_wall.forms import UserCommentForm


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


def is_new_comment_valid(
        content: str,
        user: CustomUser,
        form: UserCommentForm | GroupCommentForm,
        parent_pk: int | None,
) -> bool:
    """If the function will find any errors, they'll be added to a given form."""
    if not content:
        form.add_error('comment', 'A comment field is empty.')
        return False

    if parent_pk is not None:
        # parameter 'parent_pk' was given
        parent_comment = get_parent_comment(parent_pk=parent_pk, form=form)
        if not parent_comment:
            form.add_error(None, f'Parent comment with pk: "{parent_pk}" does not exist.')
            return False

        if parent_comment.author_id == user.pk:
            form.add_error(None, "You can't reply to your own comment.")
            return False

    return True
