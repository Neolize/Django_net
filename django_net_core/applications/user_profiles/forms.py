from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from applications.user_profiles.models import CustomUser


def define_login_field(
        label: str = 'Login',
        max_length: int = 150,
        placeholder: str = ' ',
        login_field_class: str = '',
) -> forms.CharField:
    """Return a login(username) field for a signup form"""
    login_field = forms.CharField(
        label=label,
        max_length=max_length,
        widget=forms.TextInput(
            attrs={
                'placeholder': placeholder,
                'class': login_field_class,
            }
        )
    )
    return login_field


def define_email_field(
        label: str = 'E-mail (optional)',
        min_length: int = 4,
        max_length: int = 254,
        placeholder: str = ' ',
        email_field_class: str = '',
) -> forms.EmailField:
    """Return an email field for a signup form"""
    email_field = forms.EmailField(
        label=label,
        min_length=min_length,
        max_length=max_length,
        widget=forms.EmailInput(
            attrs={
                'placeholder': placeholder,
                'class': email_field_class,
            }
        )
    )
    return email_field


def define_password_field(
        label: str = 'Password',
        min_length: int = 4,
        max_length: int = 128,
        placeholder: str = ' ',
        password_field_class: str = '',
        password_id: str = '',
) -> forms.CharField:
    """Return a password field for a signup form"""
    password_field = forms.CharField(
        label=label,
        min_length=min_length,
        max_length=max_length,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': placeholder,
                'class': password_field_class,
                'id': password_id,
            }
        )
    )
    return password_field


class SignupUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = define_login_field(login_field_class='form-signup__input')
        self.fields['email'] = define_email_field(email_field_class='form-signup__input')
        self.fields['password1'] = define_password_field(
            password_field_class='form-signup__input',
            password_id='signup-password-input',
        )
        self.fields['password2'] = define_password_field(
            label='Password (again)',
            password_field_class='form-signup__input')

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class LoginUserForm(AuthenticationForm):
    username = define_login_field(login_field_class='form-login__input')
    password = define_password_field(
        password_field_class='form-login__input',
        password_id='login-password-input',
    )


# class EditUserProfileForm(forms.Form):
#     pass

class EditUserProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=18, required=False)
    birthday = forms.DateField(required=False)
    gender = forms.CharField(max_length=13, required=False)
    address = forms.CharField(max_length=150, required=False)
    work = forms.CharField(max_length=150, required=False)
    hobby = forms.CharField(max_length=50, required=False)
    info_about_user = forms.Textarea()

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'birthday',
            'gender',
            'address',
            'work',
            'hobby',
        )
        # fields = ('username', 'email')
