from applications.user_wall import forms, models


def fill_edit_user_post_form(form: forms.UserPostForm, post: models.UserPost):
    form.fields.get('title').widget.attrs.update({'value': post.title})
    form.fields.get('tags').widget.attrs.update({'value': form_tags_string(tags=post.tags)})
    form.fields.get('content').initial = post.content
    form.fields.get('draft').widget.attrs.update({'checked': not post.is_published})


def form_tags_string(tags: models.Tag) -> str:
    tags_string = ''
    all_tags = tags.all()
    tags_number = len(all_tags) - 1
    for index, tag in enumerate(all_tags):
        if index == tags_number:
            tags_string += f'#{tag.title}'
        else:
            tags_string += f'#{tag.title}, '

    return tags_string
