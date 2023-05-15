from django.db.models import QuerySet, ObjectDoesNotExist

from applications.user_profiles import models


def get_all_users() -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.all()


def get_user_queryset_by_parameter(**kwargs) -> QuerySet[models.CustomUser]:
    return models.CustomUser.objects.filter(**kwargs)


def get_user_by_id(user_id: int) -> models.CustomUser | None:
    try:
        user = models.CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist as exc:
        print(exc)
        user = None
    return user

