import logging
from datetime import date

from django.core.files.uploadedfile import InMemoryUploadedFile

from applications.groups import models
from applications.user_profiles.models import CustomUser
from applications.user_wall.services.crud.crud_utils import return_unique_slug


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
    slug = return_unique_slug(str_for_slug=title, model=models.Group)

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
