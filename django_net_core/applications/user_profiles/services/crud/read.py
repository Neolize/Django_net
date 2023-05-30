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
        'pk',
        'username',
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


def get_user_avatar(user_pk: int) -> str:
    user = models.CustomUser.objects.get(pk=user_pk)
    return user.avatar


def fill_hobbies_str(user_data: QuerySet[dict]) -> str:
    hobbies = ''
    for index, value in enumerate(user_data):
        hobby = value.get('hobby') or ''
        if index + 1 != len(user_data):
            hobbies += f'{hobby}, '
        else:
            hobbies += hobby

    return hobbies.capitalize()


def get_user_data_for_profile_view(user_pk: int) -> dict:
    values = (
        'pk',
        'username',
        'first_name',
        'middle_name',
        'last_name',
        'email',
        'phone',
        'birthday',
        'work',
        'address',
    )
    user_data = models.CustomUser.objects.filter(pk=user_pk).annotate(
        phone=F('personal_data__phone'),
        birthday=F('personal_data__birthday'),
        work=F('personal_data__work'),
        address=F('personal_data__address'),
    ).values(*values)

    return user_data[0]
