import re
import logging

from django.db.models import QuerySet

from applications.user_profiles import models, forms
from applications.user_profiles.services.crud import delete, create


LOGGER = logging.getLogger('main_logger')


def return_error_message() -> str:
    return 'Failed to save changes. Try one more time.'


def update_user_profile_data(form: forms.EditUserProfileForm, user: models.CustomUser) -> bool:

    update_custom_user = (
            form.cleaned_data.get('first_name') or form.cleaned_data.get('middle_name') or
            form.cleaned_data.get('last_name') or form.cleaned_data.get('email') or
            form.cleaned_data.get('gender') or form.cleaned_data.get('avatar')
    )
    update_user_personal_data = (
        form.cleaned_data.get('phone') or form.cleaned_data.get('birthday') or form.cleaned_data.get('town') or
        form.cleaned_data.get('address') or form.cleaned_data.get('work') or form.cleaned_data.get('info_about_user')
    )
    update_hobby = form.cleaned_data.get('hobby')

    update_contact = (
        form.cleaned_data.get('website') or form.cleaned_data.get('github') or form.cleaned_data.get('twitter') or
        form.cleaned_data.get('instagram') or form.cleaned_data.get('facebook')
    )

    custom_user_updated, user_personal_data_updated, hobby_updated, contact_updated = (True, True, True, True)

    if update_custom_user:
        custom_user_updated = update_custom_user_model(
            form=form,
            user=user,
        )
    if update_user_personal_data:
        user_personal_data_updated = update_user_personal_data_model(
            form=form,
            user=user,
        )
    if update_hobby:
        hobby_updated = update_hobby_model(
            form=form,
            user=user,
        )
    if update_contact:
        contact_updated = update_contact_model(
            form=form,
            user=user,
        )
    return custom_user_updated and user_personal_data_updated and hobby_updated and contact_updated


def update_custom_user_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
) -> bool:

    user.first_name = form.cleaned_data.get('first_name')
    user.middle_name = form.cleaned_data.get('middle_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.gender = form.cleaned_data.get('gender')
    
    if form.cleaned_data.get('avatar'):
        user.avatar = form.cleaned_data.get('avatar')

    try:
        user.save()
        is_updated = True
    except Exception as exc:
        form.add_error(None, return_error_message())
        LOGGER.error(exc)
        is_updated = False

    return is_updated


def update_user_personal_data_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
) -> bool:

    if queryset := models.UserPersonalData.objects.filter(user=user):
        instance = queryset[0]

        instance.phone = form.cleaned_data.get('phone')
        instance.birthday = form.cleaned_data.get('birthday')
        instance.town = form.cleaned_data.get('town')
        instance.address = form.cleaned_data.get('address')
        instance.work = form.cleaned_data.get('work')
        instance.info_about_user = form.cleaned_data.get('info_about_user')

        try:
            instance.save()
            is_updated = True
        except Exception as exc:
            form.add_error(None, return_error_message())
            LOGGER.error(exc)
            is_updated = False

    else:
        is_created = create.create_user_personal_data_record(
            user_pk=user.pk,
            phone=form.cleaned_data.get('phone'),
            birthday=form.cleaned_data.get('birthday'),
            town=form.cleaned_data.get('town'),
            address=form.cleaned_data.get('address'),
            work=form.cleaned_data.get('work'),
            info_about_user=form.cleaned_data.get('info_about_user'),
        )
        if not is_created:
            form.add_error(None, return_error_message())
            is_updated = False
        else:
            is_updated = True

    return is_updated


def update_hobby_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
) -> bool:
    hobby_list = re.split(', |; ', form.cleaned_data.get('hobby').lower())
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


def update_contact_model(
        form: forms.EditUserProfileForm,
        user: models.CustomUser,
) -> bool:

    if queryset := models.Contact.objects.filter(user_id=user.pk):
        instance = queryset[0]

        instance.website = form.cleaned_data.get('website')
        instance.github = form.cleaned_data.get('github')
        instance.twitter = form.cleaned_data.get('twitter')
        instance.instagram = form.cleaned_data.get('instagram')
        instance.facebook = form.cleaned_data.get('facebook')

        try:
            instance.save()
            is_updated = True
        except Exception as exc:
            form.add_error(None, return_error_message())
            LOGGER.error(exc)
            is_updated = False

    else:
        is_created = create.create_contact_record(
            user_pk=user.pk,
            website=form.cleaned_data.get('website'),
            github=form.cleaned_data.get('github'),
            twitter=form.cleaned_data.get('twitter'),
            instagram=form.cleaned_data.get('instagram'),
            facebook=form.cleaned_data.get('facebook'),
        )
        if not is_created:
            form.add_error(None, return_error_message())
            is_updated = False
        else:
            is_updated = True

    return is_updated
