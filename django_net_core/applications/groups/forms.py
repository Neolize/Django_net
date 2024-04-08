from django import forms

from applications.groups import models


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


class GroupPostForm(forms.ModelForm):
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
                'id': 'post_id',
                'class': 'form-control user_post__tag',
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

    class Meta:
        model = models.GroupPost
        fields = ('title', 'tags', 'content', 'draft')
