from datetime import datetime

from applications.user_profiles import models, forms


def update_first_login_record(user: models.CustomUser) -> None:
    if not user.first_login:
        user.first_login = datetime.today()
        user.save()


# def update_user_profile_data(form: forms.EditUserProfileForm):
#     data = form.cleaned_data
