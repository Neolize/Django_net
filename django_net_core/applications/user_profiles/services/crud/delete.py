import logging

from applications.user_profiles import models


LOGGER = logging.getLogger('main_logger')


def delete_user_hobby(
        deleted_hobbies: list[models.Hobby],
        user: models.CustomUser,
) -> None:

    for hobby in deleted_hobbies:
        user.hobbies.remove(hobby)


def delete_follower(owner: models.CustomUser, follower: models.CustomUser) -> None:
    try:
        models.Follower.objects.get(
            user=owner,
            follower=follower,
        ).delete()
    except IndexError as exc:
        LOGGER.warning(f'Follower instance with user - {owner} and follower - {follower} was not found. {exc}')
    except Exception as exc:
        LOGGER.error(exc)
