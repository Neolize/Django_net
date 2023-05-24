from applications.user_profiles import forms


def fill_edit_user_profile_form(form: forms.EditUserProfileForm, user_data: dict) -> None:
    print(user_data)
    # filling first_name field for editing form
    form.fields.get('first_name').widget.attrs.update({'value': user_data.get('first_name')})

    # filling middle_name field for editing form
    form.fields.get('middle_name').widget.attrs.update({'value': user_data.get('middle_name')})

    # filling last_name field for editing form
    form.fields.get('last_name').widget.attrs.update({'value': user_data.get('last_name')})

    # filling email field for editing form
    form.fields.get('email').widget.attrs.update({'value': user_data.get('email')})

    # filling gender field for editing form
    form.fields.get('gender').widget.attrs.update({'data-gender': user_data.get('gender')})

    # filling phone field for editing form
    form.fields.get('phone').widget.attrs.update({'value': user_data.get('personal_data__phone')})

    # filling birthday field for editing form
    form.fields.get('birthday').widget.attrs.update({'value': user_data.get('personal_data__birthday')})

    # filling address field for editing form
    form.fields.get('address').widget.attrs.update({'value': user_data.get('personal_data__address')})

    # filling work field for editing form
    form.fields.get('work').widget.attrs.update({'value': user_data.get('personal_data__work')})

    # filling hobby field for editing form
    form.fields.get('hobby').widget.attrs.update({'value': user_data.get('hobbies__title')})

    # filling info_about_user field for editing form
    form.fields.get('info_about_user').initial = user_data.get('personal_data__info_about_user')
