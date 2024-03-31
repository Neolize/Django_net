import logging
from datetime import date

from django.core.files.uploadedfile import InMemoryUploadedFile

from applications.groups import models
from applications.user_profiles.models import CustomUser
from applications.user_wall.services.crud import crud_utils
from applications.user_wall.services.crud.create import create_tags_from_list, add_tags_to_post


LOGGER = logging.getLogger('main_logger')


def create_new_group_from_form_data(data: dict, data_files: dict, user_pk: int) -> models.Group | bool:
    return _create_new_group(
        title=data.get('title'),
        description=data.get('description'),
        logo=data_files.get('logo'),
        creator_id=user_pk,
    )


def _create_new_group(
        title: str,
        description: str,
        logo: InMemoryUploadedFile,
        creator_id: int,
) -> models.Group | bool:
    slug = crud_utils.return_unique_slug(str_for_slug=title, model=models.Group)

    try:
        new_group = models.Group.objects.create(
            title=title,
            description=description,
            logo=logo,
            creation_date=date.today(),
            slug=slug,
            creator_id=creator_id,
        )
    except Exception as exc:
        LOGGER.error(exc)
        new_group = False

    return new_group


def create_new_group_follower(group: models.Group, member: CustomUser) -> None:
    try:
        models.GroupMember.objects.create(
            member=member,
            group=group,
        )
    except Exception as exc:
        LOGGER.error(exc)


def create_group_post_from_form_date(
        data: dict,
        user_pk: int,
        group_pk: int,
) -> bool:
    is_published = not data.get('draft')
    #  group_id
    return _create_group_post(
        title=data.get('title'),
        content=data.get('content'),
        tags=data.get('tags'),
        is_published=is_published,
        author_id=user_pk,
        group_id=group_pk,
    )


def _create_group_post(
        title: str,
        content: str,
        tags: str,
        is_published: bool,
        author_id: int,
        group_id: int,
) -> bool:

    slug = crud_utils.return_unique_slug(str_for_slug=title, model=models.GroupPost)
    tags = create_tags_from_list(
        crud_utils.form_tag_list(tags)
    )
    try:
        new_group_post = models.GroupPost.objects.create(
            title=title,
            content=content,
            slug=slug,
            is_published=is_published,
            author_id=author_id,
            group_id=group_id,
        )
        add_tags_to_post(tags=tags, post=new_group_post)
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created
