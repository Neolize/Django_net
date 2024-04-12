import logging
import pytz
from datetime import datetime

from django_net_core.settings import TIME_ZONE
from applications.abstract_activities.services.crud import update as aa_update
from applications.groups import models
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
