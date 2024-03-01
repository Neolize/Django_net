import logging

from django.db.models import QuerySet, F, Q

from applications.user_profiles import models


LOGGER = logging.getLogger('main_logger')


def get_all_users() -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.all()


def get_all_users_with_personal_data():
    return models.CustomUser.objects.all().select_related('personal_data')


def fetch_users_by_names(user_input) -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.filter(
        Q(username__icontains=user_input) |
        Q(first_name__icontains=user_input) |
        Q(middle_name__icontains=user_input) |
        Q(last_name__icontains=user_input)
    )


def get_common_values_for_user_profile() -> tuple:
    return (
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
        'website',
        'github',
        'twitter',
        'instagram',
        'facebook',
    )


def get_user_data_for_edit_profile_view(user_pk: int) -> dict:
    common_values = get_common_values_for_user_profile()
    values = common_values + (
        'gender',
        'info_about_user',
        'town',
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
        website=F('contacts__website'),
        github=F('contacts__github'),
        twitter=F('contacts__twitter'),
        instagram=F('contacts__instagram'),
        facebook=F('contacts__facebook'),
    ).values(*values)

    user_data[0]['hobby'] = fill_hobbies_str(user_data)
    return user_data[0]


def fill_hobbies_str(user_data: QuerySet[dict]) -> str:
    hobbies = ''
    for index, value in enumerate(user_data):
        hobby = value.get('hobby') or ''
        if index + 1 != len(user_data):
            hobbies += f'{hobby}, '
        else:
            hobbies += hobby

    return hobbies.capitalize()


def get_user_for_profile(user_pk: int) -> models.CustomUser | bool:
    try:
        deferred_fields = (
            'password',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
            'first_login',
        )
        user_queryset = models.CustomUser.objects.filter(pk=user_pk).defer(*deferred_fields).\
            select_related('personal_data', 'contacts').prefetch_related('hobbies')
        user = user_queryset[0]
    except IndexError as exc:
        LOGGER.warning(f'User with pk - {user_pk} does not exist. {exc}')
        user = False

    return user
