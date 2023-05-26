from datetime import datetime

from django.db.models import QuerySet
from django.db.utils import DataError

from applications.user_profiles import models


def update_first_login_record(user: models.CustomUser) -> None:
    if not user.first_login:
        user.first_login = datetime.today()
        user.save()


def add_user_hobby(
        added_hobbies: QuerySet[models.Hobby],
        user: models.CustomUser,
) -> None:

    for hobby in added_hobbies:
        user.hobbies.add(hobby)


def create_new_hobby(new_hobby_title: str) -> bool:
    try:
        models.Hobby.objects.create(title=new_hobby_title.lower())
        result = True
    except DataError as exc:
        print(exc)
        result = False

    return result


def create_new_user(
        username: str,
        email: str,
        password: str,
) -> models.CustomUser | bool:

    try:
        result = models.CustomUser.objects.create_user(username=username, email=email, password=password)
    except Exception as exc:
        print(exc)
        result = False

    return result
