from django.db.models import QuerySet, F

from applications.user_profiles import models


def get_all_users() -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.all()


# def get_all_users_personal_data() -> QuerySet[models.UserPersonalData]:
#     return models.UserPersonalData.objects.all()


def is_user_with_given_pk(user_pk: int) -> bool:
    return models.CustomUser.objects.filter(pk=user_pk).exists()


def get_user_data_for_edit_profile_view(user_pk: int) -> dict:
    values = (
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'gender',
        'phone',
        'birthday',
        'info_about_user',
        'town',
        'address',
        'work',
        'hobby',
    )
    user_data = models.CustomUser.objects.filter(pk=user_pk).annotate(
        phone=F('personal_data__phone'),
        birthday=F('personal_data__birthday'),
        info_about_user=F('personal_data__info_about_user'),
        town=F('personal_data__town'),
        address=F('personal_data__address'),
        work=F('personal_data__work'),
        hobby=F('hobbies__title'),
    ).values(*values)

    user_data[0]['hobby'] = fill_hobbies_str(user_data)
    return user_data[0]


def fill_hobbies_str(user_data: QuerySet[dict]) -> str:
    hobbies = ''
    for index, value in enumerate(user_data):
        if index + 1 != len(user_data):
            hobbies += f'{value.get("hobby")}, '
        else:
            hobbies += value.get('hobby')

    return hobbies


def get_user_data(user_pk: int, profile: bool = True) -> dict:
    base_values = (
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'gender'
    )
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
            'personal_data__town',
            'personal_data__address',
            'personal_data__work',
            'hobbies__title',
        )
    }
    if profile:
        values = base_values + values_dict['profile']
    else:
        values = base_values + values_dict['edit']

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
