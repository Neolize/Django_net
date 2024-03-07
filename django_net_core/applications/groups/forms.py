from django import forms


class CreateGroup(forms.Form):
    title = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    description = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
            }
        )
    )
    logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
