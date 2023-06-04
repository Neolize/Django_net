from django import forms


class PostCreationForm(forms.Form):
    title = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Start your tags with # and write them separated by commas',
            }
        )
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'form-edit__info_about_user',
                'rows': '10',
            }
        )
    )
    draft = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-draft',
            }
        )
    )
