import logging
import pytz
from datetime import datetime

from django_net_core.settings import TIME_ZONE
from applications.abstract_activities.services.crud import update
from applications.user_wall import models
from applications.user_wall.services.crud import crud_utils, create


LOGGER = logging.getLogger('main_logger')


def update_user_post(data: dict, post: models.UserPost) -> bool:
    is_published = not data.get('draft')
    new_title = data.get('title')
    new_tags = crud_utils.form_tag_list(data.get('tags'))
    old_tags = [tag.title for tag in post.tags.all()]

    if not update.is_post_changed(
        post=post,
        new_title=new_title,
        new_content=data.get('content'),
        new_tags=new_tags,
        old_tags=old_tags,
        is_published=is_published,
    ):
        return True

    if new_tag_list := update.return_new_tag_list(
        new_tags=new_tags,
        old_tags=old_tags,
        post=post,
    ):
        tags = create.return_tag_objects_from_list(new_tag_list)
    else:
        tags = []

    if post.title != new_title:
        slug = crud_utils.return_unique_slug(str_for_slug=new_title, model=models.UserPost)
    else:
        slug = post.slug

    dt = datetime.now()
    time_zone = pytz.timezone(TIME_ZONE)

    try:
        post.title = new_title
        post.content = data.get('content')
        post.slug = slug
        post.is_published = is_published
        post.last_edit = time_zone.localize(dt)

        create.add_tags_to_post(tags=tags, post=post)
        post.save()
        is_edited = True
    except Exception as exc:
        LOGGER.error(exc)
        is_edited = False

    return is_edited
