from django.db.models import QuerySet

from applications.user_profiles import models


def get_all_users() -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.all()


# def get_all_users_personal_data() -> QuerySet[models.UserPersonalData]:
#     return models.UserPersonalData.objects.all()


def is_user_with_given_pk(user_pk: int) -> bool:
    return models.CustomUser.objects.filter(pk=user_pk).exists()


def get_user_data(user_pk: int, profile: bool = True) -> dict:
    values_dict = {
        'profile': (
            'personal_data__phone',
            'personal_data__birthday',
            'personal_data__address',
        ),
        'edit': (
            'personal_data__phone',
            'personal_data__birthday',
            'personal_data__info_about_user',
            'personal_data__address',
            'personal_data__work',
            'hobbies__title',
        )
    }
    if profile:
        values = values_dict['profile']
    else:
        values = values_dict['edit']

    return models.CustomUser.objects.filter(pk=user_pk).values(*values)[0]


# def get_user_data_for_profile(user_pk: int) -> dict:
#     user_data = models.CustomUser.objects.filter(pk=user_pk)
#
#
# def get_user_data_for_editing(user_pk: int) -> dict:
#     user_data = models.CustomUser.objects.filter(pk=user_pk).values(
#         'personal_data__phone',
#         'personal_data__birthday',
#         'personal_data__info_about_user',
#         'personal_data__address',
#         'personal_data__work',
#         'hobbies__title',
#     )
#     if user_data:
#         return user_data[0]


# def get_user_by_pk(user_pk: int) -> models.CustomUser | None:
#     try:
#         user = models.CustomUser.objects.get(pk=user_pk)
#     except ObjectDoesNotExist as exc:
#         user = None
#         print(exc)
#
#     return user
