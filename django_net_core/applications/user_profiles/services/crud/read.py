from django.db.models import QuerySet, ObjectDoesNotExist

from applications.user_profiles import models


def get_all_users() -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.all()


def get_all_users_personal_data() -> QuerySet[models.UserPersonalData]:
    return models.UserPersonalData.objects.all()


# def get_user_queryset_by_parameter(**kwargs) -> QuerySet[models.CustomUser]:
#     return models.CustomUser.objects.filter(**kwargs)


def get_user_by_pk(user_pk: int) -> models.CustomUser | None:
    try:
        user = models.CustomUser.objects.get(pk=user_pk)
    except ObjectDoesNotExist as exc:
        user = None
        print(exc)

    return user
