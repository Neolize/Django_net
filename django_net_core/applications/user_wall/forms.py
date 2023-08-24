from django import forms

from applications.user_wall import models


class UserPostForm(forms.ModelForm):
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
        model = models.UserPost
        fields = ('title', 'tags', 'content', 'draft')


class UserCommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control rounded',
                'style': 'margin-right: 10px',
                'placeholder': 'Write a comment...',
                'rows': 1,
                'id': 'usercomment-input',
            }
        )
    )

    class Meta:
        model = models.UserComment
        fields = ('comment', )
