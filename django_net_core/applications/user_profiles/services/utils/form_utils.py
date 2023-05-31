from applications.user_profiles import forms


def fill_edit_user_profile_form(form: forms.EditUserProfileForm, user_data: dict) -> None:
    """Fill all fields for editing form with gotten values from user's model"""
    special_fields = ('gender', 'info_about_user')  # these fields should be filled separately

    for field in form.fields:
        if field not in special_fields:
            current_value = user_data.get(field) or ''
            form.fields.get(field).widget.attrs.update({'value': current_value})

    # filling data-gender attribute in gender field for editing form
    form.fields.get('gender').widget.attrs.update({'data-gender': user_data.get('gender')})

    # filling info_about_user field for editing form
    info_about_user = user_data.get('info_about_user') or ''
    form.fields.get('info_about_user').initial = info_about_user
