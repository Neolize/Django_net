import logging

from django.db.models import QuerySet

from applications.abstract_activities.models import AbstractPost
from applications.abstract_activities.services.utils import get_parent_comment

from applications.frontend.permissions import is_user_comment_author

from applications.groups.models import GroupPost, GroupComment
from applications.groups.forms import GroupCommentForm

from applications.user_profiles.models import CustomUser

from applications.user_wall.models import UserPost, UserComment
from applications.user_wall.forms import UserCommentForm
from applications.user_wall.services.crud.delete import delete_tag_from_post


LOGGER = logging.getLogger('main_logger')


def update_posts_view_count(
        creator_pk: int,
        visitor_pk: int,
        posts: QuerySet[AbstractPost]
) -> None:
    if visitor_pk == creator_pk:
        return None

    for post in posts:
        if visitor_pk not in post.user_list:
            # increase counter when the appropriate page is opened
            post.view_counts += 1
            post.user_list.append(visitor_pk)
            post.save()


def is_post_changed(
        post: AbstractPost,
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


def return_new_tag_list(
        new_tags: list[str],
        old_tags: list[str],
        post: UserPost | GroupPost,
) -> list[str]:
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
                delete_tag_from_post(tag_title=tag, post=post)
        return new_tags

    return added_tags_list


def update_comment(
        comment: UserComment | GroupComment,
        content: str,
        author_id: int,
        post_id: int,
        parent_id: int | None,
) -> bool:
    try:
        comment.content = content
        comment.author_id = author_id
        comment.post_id = post_id
        comment.parend_id = parent_id
        comment.is_edited = True
        comment.save()

        is_updated = True
    except Exception as exc:
        LOGGER.error(exc)
        is_updated = False

    return is_updated


def is_edited_comment_valid(
        new_content: str,
        comment: UserComment | GroupComment | bool,
        comment_pk: int,
        user: CustomUser,
        form: UserCommentForm | GroupCommentForm,
        parent_pk: int | None,
) -> bool:
    """If the function will find any errors, they'll be added to a given form."""
    if not comment:
        form.add_error(None, f'A comment with pk: "{comment_pk}" does not exist.')
        return False

    if not comment.author_id:
        form.add_error(None, "You can't update this comment.")
        return False

    if not is_user_comment_author(visitor=user, comment=comment):
        form.add_error(None, 'You are not an author of this comment.')
        return False

    if not new_content:
        form.add_error('comment', 'A "comment" field is empty.')
        return False

    if new_content == comment.content:
        form.add_error('comment', "The comment hasn't changed.")
        return False

    if parent_pk is not None:
        # parameter 'parent_pk' was given
        parent_comment = get_parent_comment(parent_pk=parent_pk, form=form)
        if not parent_comment:
            form.add_error(None, f'Parent comment with pk: "{parent_pk}" does not exist.')
            return False

        if not parent_comment.author_id:
            form.add_error(None, "You can't update this comment.")
            return False

        if parent_comment.author_id == user.pk:
            form.add_error(None, "You can't reply to your own comment.")
            return False

    return True
