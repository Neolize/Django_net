import logging
import pytz
from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest

from django_net_core.settings import TIME_ZONE
from applications.abstract_activities.services.crud import update as aa_update
from applications.frontend.permissions import is_user_comment_author
from applications.groups import models, forms
from applications.groups.services.crud.read import get_group_comment_by_pk
from applications.user_profiles.models import CustomUser
from applications.user_wall.services.crud import crud_utils
from applications.user_wall.services.crud import create as uw_create


LOGGER = logging.getLogger('main_logger')


def update_group_post(data: dict, group_post: models.GroupPost) -> bool:
    is_published = not data.get('draft')
    new_title = data.get('title')
    new_tags = crud_utils.form_tag_list(data.get('tags'))
    old_tags = [tag.title for tag in group_post.tags.all()]

    if not aa_update.is_post_changed(
        post=group_post,
        new_title=new_title,
        new_content=data.get('content'),
        new_tags=new_tags,
        old_tags=old_tags,
        is_published=is_published,
    ):
        return True

    if new_tag_list := aa_update.return_new_tag_list(
        new_tags=new_tags,
        old_tags=old_tags,
        post=group_post,
    ):
        tags = uw_create.return_tag_objects_from_list(new_tag_list)
    else:
        tags = []

    if group_post.title != new_title:
        slug = crud_utils.return_unique_slug(str_for_slug=new_title, model=models.GroupPost)
    else:
        slug = group_post.slug

    dt = datetime.now()
    time_zone = pytz.timezone(TIME_ZONE)

    try:
        group_post.title = new_title
        group_post.content = data.get('content')
        group_post.slug = slug
        group_post.is_published = is_published
        group_post.last_edit = time_zone.localize(dt)

        uw_create.add_tags_to_post(tags=tags, post=group_post)
        group_post.save()
        is_edited = True
    except Exception as exc:
        LOGGER.error(exc)
        is_edited = False

    return is_edited


def update_group_comment(
        form: forms.GroupCommentForm,
        request: WSGIRequest,
        comment_pk: int,
) -> bool:
    comment = get_group_comment_by_pk(comment_pk)
    content = form.cleaned_data.get('comment', '')
    post_id = int(request.POST.get('post_id'))
    parent_id = int(request.POST.get('parent_id')) if request.POST.get('parent_id') else None

    # if not comment or not is_user_comment_author(visitor=request.user, comment=comment):
    #     return False
    #
    # if not content or content == comment.content:
    #     return False    # comment hasn't changed or doesn't have a 'content' field

    # post_id = int(request.POST.get('post_id'))
    # parent_id = int(request.POST.get('parent_id')) if request.POST.get('parent_id') else None

    return aa_update.update_comment(
        comment=comment,
        content=content,
        author_id=request.user.pk,
        post_id=post_id,
        parent_id=parent_id,
    )
#
#     if not _is_edited_user_comment_valid(
#         content=content,
#         comment=comment,
#         form=form,
#         user=request.user,
#         parent_pk=parent_id,
#     ):
#         return False
#
#     is_updated = update.update_comment(
#         comment=comment,
#         content=content,
#         author_id=request.user.pk,
#         post_id=post_id,
#         parent_id=parent_id,
#     )
#     if not is_updated:
#         form.add_error(None, 'An error occurred during a comment creation. Try one more time.')
#
#     return is_updated


def _is_edited_group_comment_valid(
        new_content: str,
        comment: models.GroupComment | bool,
        comment_pk: int,
        user: CustomUser,
        form: forms.GroupCommentForm,
        parent_pk: int,
) -> bool:
    """If the function will find any errors, they'll be added to a given form."""
    if not comment:
        form.add_error(None, f'A comment with pk: "{comment_pk}" does not exist.')
        return False

    if not is_user_comment_author(visitor=user, comment=comment):
        form.add_error(None, 'You are not an author of this comment.')
        return False

    if not new_content:
        form.add_error('comment', 'A comment field is empty.')
        return False

    if new_content == comment.content:
        form.add_error('comment', "The comment hasn't changed.")
        return False

    parent_comment = get_group_comment_by_pk(parent_pk)
    if not parent_comment:
        form.add_error(None, f'Parent comment with pk: "{parent_pk}" does not exist.')

# def _is_edited_user_comment_valid(
#         content: str,
#         comment: models.UserComment | bool,
#         user: CustomUser,
#         form: forms.UserCommentForm,
#         parent_pk: int,
# ) -> bool:
#     """If the function will find any errors, they'll be added to a given form."""
#
#     parent_comment = read.get_user_comment_by_pk(parent_pk)
#     if not parent_comment:
#         form.add_error(None, f'Parent comment with pk: "{parent_pk}" does not exist.')
#         return False
#
#     if parent_comment.author_id == comment.author_id:
#         form.add_error(None, "You can't reply to your own comment.")
#         return False
#
#     return True
