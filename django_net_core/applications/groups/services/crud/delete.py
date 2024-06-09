import logging

from rest_framework.serializers import SerializerMetaclass

from applications.groups import models, serializers as g_serializers
from applications.user_profiles.models import CustomUser


LOGGER = logging.getLogger('main_logger')


def delete_group_follower(group: models.Group, member: CustomUser) -> None:
    try:
        models.GroupMember.objects.get(
            member=member,
            group=group,
        ).delete()
    except IndexError as exc:
        LOGGER.warning(f'Group instance with member - {member} and group - {group} was not found. {exc}')
    except Exception as exc:
        LOGGER.error(exc)


def delete_group_instance(group: models.Group) -> bool:
    try:
        group.delete()
        deleted = True
    except Exception as exc:
        LOGGER.error(exc)
        deleted = False

    return deleted


def delete_group_from_api_request(
        serializer: SerializerMetaclass,
        instance: models.Group
) -> g_serializers.GroupDeletionSerializer:
    serializer = serializer(instance=instance)
    serializer.delete(instance=instance)
    return serializer
