import logging
from datetime import datetime, date

from django.db.models import QuerySet
from django.db.utils import DataError

from applications.user_profiles import models


LOGGER = logging.getLogger('main_logger')


def update_first_login_record(user: models.CustomUser) -> None:
    if not user.first_login:
        user.first_login = datetime.today()
        user.save()


def add_user_hobby(new_hobbies: QuerySet[models.Hobby], user: models.CustomUser) -> None:
    for hobby in new_hobbies:
        user.hobbies.add(hobby)


def create_new_hobby(new_hobby_title: str) -> bool:
    try:
        models.Hobby.objects.create(title=new_hobby_title.lower())
        is_created = True
    except DataError as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created


def create_new_user(
        username: str,
        email: str,
        password: str,
) -> models.CustomUser | bool:

    try:
        is_created = models.CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created


def create_user_personal_data_record(
        user_pk: int,
        phone: str,
        birthday: date,
        town: str,
        address: str,
        work: str,
        info_about_user: str,
) -> bool:
    try:
        models.UserPersonalData.objects.create(
            phone=phone,
            birthday=birthday,
            town=town,
            address=address,
            work=work,
            info_about_user=info_about_user,
            user_id=user_pk,
        )
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created


def create_contact_record(
        user_pk: int,
        website: str,
        github: str,
        twitter: str,
        instagram: str,
        facebook: str,
) -> bool:
    try:
        models.Contact.objects.create(
            website=website,
            github=github,
            twitter=twitter,
            instagram=instagram,
            facebook=facebook,
            user_id=user_pk,
        )
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created
