import re
from datetime import datetime, date

from applications.user_profiles import models, forms


def update_first_login_record(user: models.CustomUser) -> None:
    if not user.first_login:
        user.first_login = datetime.today()
        user.save()


def update_user_profile_data(form: forms.EditUserProfileForm, user: models.CustomUser) -> bool:
    form_data = form.cleaned_data

    update_custom_user = (
            form_data.get('first_name') or form_data.get('middle_name') or
            form_data.get('last_name') or form_data.get('email') or
            form_data.get('gender')
    )
    update_user_personal_data = (
        form_data.get('phone') or form_data.get('birthday') or
        form_data.get('town') or form_data.get('address') or
        form_data.get('work') or form_data.get('info_about_user')
    )
    update_hobby = form_data.get('hobby')

    first_result, second_result, third_result = (True, True, True)

    if update_custom_user:
        first_result = update_custom_user_model(
            form=form,
            user=user,
            first_name=form_data.get('first_name'),
            middle_name=form_data.get('middle_name'),
            last_name=form_data.get('last_name'),
            email=form_data.get('email'),
            gender=form_data.get('gender'),
        )
    if update_user_personal_data:
        second_result = update_user_personal_data_model(
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
        third_result = update_hobby_model(
            form=form,
            user=user,
            hobby=form_data.get('hobby'),
        )

    return first_result and second_result and third_result


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

    if instance := models.UserPersonalData.objects.filter(user=user).exists():
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

    hobby_list = re.split(', |; | ', hobby)
    result = True

    for hobby_item in hobby_list:

        if instance := models.Hobby.objects.filter(title=hobby_item).exists():
            # instance.users.add(user)
            user.hobbies.add(instance)

            try:
                instance.save()
                result = True
            except Exception as exc:
                form.add_error(None, exc)
                print(exc)
                result = False

        else:
            try:
                new_instance = models.Hobby.objects.create(title=hobby)
                new_instance.users.add(user)
                new_instance.save()
                result = True
            except Exception as exc:
                form.add_error(None, exc)
                print(exc)
                result = False

    return result
