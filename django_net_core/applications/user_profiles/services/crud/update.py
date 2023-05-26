import re
from datetime import date

from django.db.models import QuerySet

from applications.user_profiles import models, forms
from applications.user_profiles.services.crud import delete, create


def update_user_profile_data(form: forms.EditUserProfileForm, user: models.CustomUser) -> bool:
    form_data = form.cleaned_data

    update_custom_user = (
            form_data.get('first_name') or form_data.get('middle_name') or form_data.get('last_name') or
            form_data.get('email') or form_data.get('gender')
    )
    update_user_personal_data = (
        form_data.get('phone') or form_data.get('birthday') or form_data.get('town') or
        form_data.get('address') or form_data.get('work') or form_data.get('info_about_user')
    )
    update_hobby = form_data.get('hobby')

    custom_user_updated, user_personal_data_updated, hobby_updated = (True, True, True)

    if update_custom_user:
        custom_user_updated = update_custom_user_model(
            form=form,
            user=user,
            first_name=form_data.get('first_name'),
            middle_name=form_data.get('middle_name'),
            last_name=form_data.get('last_name'),
            email=form_data.get('email'),
            gender=form_data.get('gender'),
        )
    if update_user_personal_data:
        user_personal_data_updated = update_user_personal_data_model(
            form=form,
            user=user,
            phone=form_data.get('phone'),
            birthday=form_data.get('birthday'),
            town=form_data.get('town'),
            address=form_data.get('address'),
            work=form_data.get('work'),
            info_about_user=form_data.get('info_about_user'),
        )
    if update_hobby:
        hobby_updated = update_hobby_model(
            form=form,
            user=user,
            hobby=form_data.get('hobby'),
        )
    return custom_user_updated and user_personal_data_updated and hobby_updated


def update_custom_user_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
        first_name: str,
        middle_name: str,
        last_name: str,
        email: str,
        gender: str,
) -> bool:

    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name = last_name
    user.email = email
    user.gender = gender

    try:
        user.save()
        result = True
    except Exception as exc:
        form.add_error(None, exc)
        print(exc)
        result = False

    return result


def update_user_personal_data_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
        phone: str,
        birthday: date,
        town: str,
        address: str,
        work: str,
        info_about_user: str,
) -> bool:

    if instance_queryset := models.UserPersonalData.objects.filter(user=user):
        instance = instance_queryset[0]

        instance.phone = phone
        instance.birthday = birthday
        instance.town = town
        instance.address = address
        instance.work = work
        instance.info_about_user = info_about_user

        try:
            instance.save()
            result = True
        except Exception as exc:
            form.add_error(None, exc)
            print(exc)
            result = False

    else:
        try:
            models.UserPersonalData.objects.create(
                phone=phone,
                birthday=birthday,
                town=town,
                address=address,
                work=work,
                info_about_user=info_about_user,
                user_id=user.pk,
            )
            result = True
        except Exception as exc:
            form.add_error(None, exc)
            print(exc)
            result = False

    return result


def update_hobby_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
        hobby: str,
) -> bool:
    hobby_list = re.split(', |; ', hobby.lower())
    current_hobby_set = models.Hobby.objects.filter(users__in=[user])

    if new_hobbies := return_new_hobby_list(hobby_list):
        for new_hobby in new_hobbies:
            if not create.create_new_hobby(new_hobby):
                form.add_error('hobby', f'Your hobby title is too long. Shorten this to 50 characters.')
                return False

    if deleted_hobbies := return_deleted_hobbies(current_hobby_set=current_hobby_set, new_hobby_list=hobby_list):
        delete.delete_user_hobby(
            deleted_hobbies=deleted_hobbies,
            user=user,
        )
    elif added_hobbies := return_added_hobbies(current_hobby_set=current_hobby_set, new_hobby_list=hobby_list):
        create.add_user_hobby(
            added_hobbies=added_hobbies,
            user=user,
        )


def return_new_hobby_list(hobby_list: list[str]) -> list[str]:
    all_hobbies_set = set(models.Hobby.objects.all().values_list('title', flat=True))
    new_hobbies_set = set(hobby_list)
    return list(new_hobbies_set.difference(all_hobbies_set))


def return_deleted_hobbies(
        current_hobby_set: QuerySet[models.Hobby],
        new_hobby_list: list[str]
) -> list[models.Hobby]:
    result = []
    for hobby in current_hobby_set:
        if hobby.title not in new_hobby_list:
            result.append(hobby)

    return result


def return_added_hobbies(
        current_hobby_set: QuerySet[models.Hobby],
        new_hobby_list: list[str],
) -> QuerySet[models.Hobby]:
    added_hobbies = []
    current_hobby_list = [hobby.title for hobby in current_hobby_set]
    for hobby in new_hobby_list:
        if hobby not in current_hobby_list:
            added_hobbies.append(hobby)

    return models.Hobby.objects.filter(title__in=added_hobbies)
