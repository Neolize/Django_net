import logging

from django.db.models import QuerySet, F, Q

from applications.user_profiles import models
from applications.groups.models import Group


LOGGER = logging.getLogger('main_logger')


def get_all_users() -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.all()


def get_all_users_with_personal_data() -> QuerySet[models.CustomUser]:
    """Return all users with all needed information"""
    return (
        models.CustomUser.objects.all().order_by('pk').
        select_related(
            'personal_data',
            'contacts'
        ).
        prefetch_related(
            'followers',
            'user_comments',
            'user_groups',
            'group_comments',
        )
    )


def fetch_users_by_names(user_input) -> QuerySet[models.CustomUser]:
    """Return users selected by names with all needed information"""
    return (
        models.CustomUser.objects.filter(
            Q(username__icontains=user_input) |
            Q(first_name__icontains=user_input) |
            Q(middle_name__icontains=user_input) |
            Q(last_name__icontains=user_input)
        ).order_by('pk').
        select_related(
            'personal_data',
            'contacts'
        ).
        prefetch_related(
            'followers',
            'user_comments',
            'user_groups',
            'group_comments',
        )
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
            select_related(
            'personal_data',
            'contacts'
        ).prefetch_related(
            'hobbies',
            'followers',
            'owner',
        )
        user = user_queryset[0]
    except IndexError as exc:
        LOGGER.warning(f'User with pk - {user_pk} does not exist. {exc}')
        user = False

    return user


def get_raw_user_instance(user_pk: int) -> models.CustomUser | bool:
    try:
        user = models.CustomUser.objects.get(pk=user_pk)
    except IndexError as exc:
        LOGGER.warning(f'User with pk - {user_pk} does not exist. {exc}')
        user = False

    return user


def fetch_all_user_followers(user: models.CustomUser) -> QuerySet[models.Follower]:
    return (
        user.followers.all().select_related(
            'follower',
            'follower__personal_data',
            'follower__contacts',
        ).
        prefetch_related(
            'follower__followers',
            'follower__user_comments',
            'follower__user_groups',
            'follower__group_comments',
        )
    )


def fetch_user_for_followers_page(user_pk: int) -> models.CustomUser | bool:
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
            select_related('personal_data', 'contacts')
        user = user_queryset[0]
    except IndexError as exc:
        LOGGER.warning(f'User with pk - {user_pk} does not exist. {exc}')
        user = False

    return user


def fetch_all_user_followings(user: models.CustomUser) -> QuerySet[models.CustomUser]:
    return (
        user.owner.all().select_related(
            'user',
            'user__personal_data',
            'user__contacts',
        ).
        prefetch_related(
            'user__followers',
            'user__user_comments',
            'user__user_groups',
            'user__group_comments',
        )
    )


def get_published_user_posts_number(user_obj: models.CustomUser) -> int:
    """The function returns the number of published posts."""
    try:
        posts_number = user_obj.user_posts.filter(is_published=True).count()
    except Exception as exc:
        LOGGER.error(exc)
        posts_number = 0

    return posts_number


def get_all_user_posts_number(user_obj: models.CustomUser) -> int:
    """The function returns the number of all posts."""
    try:
        posts_number = user_obj.user_posts.all().count()
    except Exception as exc:
        LOGGER.error(exc)
        posts_number = 0

    return posts_number


def get_followers_number_from_user_obj(user_obj: models.CustomUser) -> int:
    try:
        followers = user_obj.followers.count()
    except Exception as exc:
        LOGGER.error(exc)
        followers = 0

    return followers


def get_following_number_from_user_obj(user_obj: models.CustomUser) -> int:
    try:
        following = user_obj.owner.count()
    except Exception as exc:
        LOGGER.error(exc)
        following = 0

    return following


def get_all_groups_from_user_obj(user_obj: models.CustomUser) -> QuerySet[Group] | list:
    try:
        groups = user_obj.user_groups.all()
    except Exception as exc:
        LOGGER.error(exc)
        groups = []

    return groups
