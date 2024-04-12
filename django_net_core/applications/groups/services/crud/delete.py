import logging

from applications.groups import models
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
