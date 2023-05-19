from django import forms

from allauth.account.forms import LoginForm, SignupForm

from applications.user_profiles.models import GENDER_CHOICES


def define_login_field(
        maxlength: int = 150,
        placeholder: str = 'Login *',
        autocomplete: str = 'username',
        login_field_class: str = 'account-input account-signup-login',
) -> forms.CharField:
    """Return a login(username) field for a signup form"""
    login_field = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': maxlength,
                'placeholder': placeholder,
                'autocomplete': autocomplete,
                'class': login_field_class,
            }
        )
    )
    return login_field


def define_email_field(
        min_length: int = 4,
        max_length: int = 254,
        placeholder: str = 'E-mail address (optional)',
        autocomplete: str = 'email',
        email_field_class: str = 'account-input account-signup-email',
) -> forms.EmailField:
    """Return an email field for a signup form"""
    email_field = forms.EmailField(
        min_length=min_length,
        max_length=max_length,
        widget=forms.EmailInput(
            attrs={
                'placeholder': placeholder,
                'autocomplete': autocomplete,
                'class': email_field_class,
            }
        )
    )
    return email_field

#         widget=forms.TextInput(
#             attrs={
#                 "type": "email",
#                 "required": True,
#                 "placeholder": " ",
#                 "autocomplete": f"{custom_autocomplete}",
#                 "class": f"{custom_class}",
#                 "id": f"{custom_id}"
# attrs={"class": "form-control border", "maxlength": "10",
#                                                      "required": True, "placeholder": "format: \"YYYY-MM-DD\"",
#                                                      "id": "id_world_premiere", "name": "world_premiere"},


def define_password_field(
        min_length: int = 8,
        max_length: int = 128,
        placeholder: str = 'Password *',
        autocomplete: str = 'password',
        password_field_class: str = 'account-input account-signup-password',
) -> forms.CharField:
    """Return a password field for a signup form"""
    password_field = forms.CharField(
        min_length=min_length,
        max_length=max_length,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': placeholder,
                'autocomplete': autocomplete,
                'class': password_field_class,
            }
        )
    )
    return password_field


def define_phone_field(
        required: bool = False,
        placeholder: str = 'Phone number (optional)',
        autocomplete: str = 'phone',
        maxlength: int = 18,
        phone_field_class: str = 'account-input account-signup-phone',
) -> forms.CharField:
    """Return a phone field for a signup form"""
    phone_field = forms.CharField(
        required=required,
        widget=forms.TextInput(
            attrs={
                'placeholder': placeholder,
                'autocomplete': autocomplete,
                'maxlength': maxlength,
                'class': phone_field_class,
            }
        )
    )
    return phone_field


def define_town_field(
        required: bool = False,
        placeholder: str = 'City (optional)',
        autocomplete: str = 'town',
        maxlength: int = 60,
        town_field_class: str = 'account-input account-signup-town',
) -> forms.CharField:
    """Return a town field for a signup form"""
    town_field = forms.CharField(
        required=required,
        widget=forms.TextInput(
            attrs={
                'placeholder': placeholder,
                'autocomplete': autocomplete,
                'maxlength': maxlength,
                'class': town_field_class,
            }
        )
    )
    return town_field


def define_birthday_field(
        required: bool = False,
        placeholder: str = 'format: YYYY-MM-DD (optional)',
        maxlength: int = 10,
        birthday_field_class: str = 'account-input account-signup-birthday',
) -> forms.DateField:
    """Return a birthday field for a signup form"""
    birthday_field = forms.DateField(
        required=required,
        widget=forms.DateInput(
            attrs={
                'placeholder': placeholder,
                'maxlength': maxlength,
                'class': birthday_field_class,
            }
        )
    )
    return birthday_field


def define_gender_field(
        required: bool = False,
        gender_field_class: str = 'account-input account-signup-gender',
) -> forms.ChoiceField:
    """Return a gender field for a signup form"""
    gender_field = forms.ChoiceField(
        required=required,
        widget=forms.Select(
            attrs={
                'class': gender_field_class,
            }
        ),
        choices=GENDER_CHOICES,
        initial='not specified',
    )
    return gender_field


class SignupUserForm(SignupForm):
    username = define_login_field()
    email = define_email_field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'] = define_password_field()
        self.fields['password2'] = define_password_field(
            placeholder='Password (again) *',
        )
        self.fields['phone'] = define_phone_field()
        self.fields['town'] = define_town_field()
        self.fields['birthday'] = define_birthday_field()
        self.fields['gender'] = define_gender_field()


class LoginUserForm(LoginForm):
    pass
