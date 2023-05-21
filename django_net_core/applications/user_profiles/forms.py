from django import forms
from django.contrib.auth.forms import AuthenticationForm

from allauth.account.forms import SignupForm

from applications.user_profiles.models import GENDER_CHOICES
from applications.user_profiles.services import utils


def define_login_field(
        label: str = 'Login',
        maxlength: int = 150,
        placeholder: str = 'Login',
        autocomplete: str = 'username',
        login_field_class: str = 'account-input account-signup-login',
) -> forms.CharField:
    """Return a login(username) field for a signup form"""
    login_field = forms.CharField(
        label=label,
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
        label: str = 'E-mail (optional)',
        min_length: int = 4,
        max_length: int = 254,
        placeholder: str = 'E-mail address',
        autocomplete: str = 'email',
        email_field_class: str = 'account-input account-signup-email',
) -> forms.EmailField:
    """Return an email field for a signup form"""
    email_field = forms.EmailField(
        label=label,
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


def define_password_field(
        label: str = 'Password',
        min_length: int = 8,
        max_length: int = 128,
        placeholder: str = 'Password',
        autocomplete: str = 'password',
        password_field_class: str = 'account-input account-signup-password',
) -> forms.CharField:
    """Return a password field for a signup form"""
    password_field = forms.CharField(
        label=label,
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
        label: str = 'Phone (optional)',
        required: bool = False,
        placeholder: str = 'Phone number (optional)',
        autocomplete: str = 'phone',
        maxlength: int = 18,
        phone_field_class: str = 'account-input account-signup-phone',
) -> forms.CharField:
    """Return a phone field for a signup form"""
    phone_field = forms.CharField(
        label=label,
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
        label: str = 'Town (optional)',
        required: bool = False,
        placeholder: str = 'City (optional)',
        autocomplete: str = 'town',
        maxlength: int = 60,
        town_field_class: str = 'account-input account-signup-town',
) -> forms.CharField:
    """Return a town field for a signup form"""
    town_field = forms.CharField(
        label=label,
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
        label: str = 'Brith date',
        required: bool = False,
        birthday_field_class: str = 'account-input account-signup-birthday',
) -> forms.DateField:
    """Return a birthday field for a signup form"""
    birthday_field = forms.DateField(
        label=label,
        required=required,
        initial=utils.get_current_date(),
        widget=forms.SelectDateWidget(
            attrs={
                'class': birthday_field_class,
            },
            years=utils.get_range_of_years(),
        )
    )
    return birthday_field


def define_gender_field(
        label: str = 'Gender (optional)',
        required: bool = False,
        gender_field_class: str = 'account-input account-signup-gender',
) -> forms.ChoiceField:
    """Return a gender field for a signup form"""
    gender_field = forms.ChoiceField(
        label=label,
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
            label='Password (again)',
            placeholder='Password',
        )
        self.fields['phone'] = define_phone_field()
        self.fields['town'] = define_town_field()
        self.fields['birthday'] = define_birthday_field()
        self.fields['gender'] = define_gender_field()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Login',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': ' ',
                'class': 'form-login__input',
            }
        )
    )
    password = forms.CharField(
        label='Password',
        min_length=4,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': ' ',
                'class': 'form-login__input',
                'id': 'login-password-input',
            }
        )
    )
