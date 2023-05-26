from applications.user_profiles import models


def delete_user_hobby(
        deleted_hobbies: list[models.Hobby],
        user: models.CustomUser,
) -> None:

    for hobby in deleted_hobbies:
        user.hobbies.remove(hobby)
