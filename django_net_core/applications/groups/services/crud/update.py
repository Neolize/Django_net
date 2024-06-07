import logging
import pytz
from datetime import datetime

from rest_framework.request import Request
from rest_framework.serializers import SerializerMetaclass
from django.core.handlers.wsgi import WSGIRequest

from django_net_core.settings import TIME_ZONE
from applications.abstract_activities.services.crud import update as aa_update
from applications.groups import models, forms, serializers as g_serializers
from applications.groups.services.crud.read import get_group_comment_by_pk
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
) -> bool:

    comment_pk = int(request.POST.get('comment_id', 0))
    comment = get_group_comment_by_pk(comment_pk)

    content = form.cleaned_data.get('comment', '')
    post_id = int(request.POST.get('post_id', 0))
    parent_id = int(request.POST.get('parent_id')) if request.POST.get('parent_id') else None

    if not aa_update.is_edited_comment_valid(
        new_content=content,
        comment=comment,
        comment_pk=comment_pk,
        form=form,
        user=request.user,
        parent_pk=parent_id,
    ):
        return False

    is_updated = aa_update.update_comment(
        comment=comment,
        content=content,
        author_id=request.user.pk,
        post_id=post_id,
        parent_id=parent_id,
    )
    if not is_updated:
        form.add_error(None, 'An error occurred during a comment editing. Try one more time.')

    return is_updated


def update_group_from_api_request(
        request: Request,
        serializer: SerializerMetaclass,
        instance: models.Group
) -> g_serializers.GroupSerializer:
    serializer = serializer(data=request.data, instance=instance)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer
