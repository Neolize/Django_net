from django.db.models import QuerySet
from django.db.models.base import ModelBase

from applications.groups.models import GroupPost
from applications.groups.forms import GroupPostForm

from applications.user_wall.models import Tag, UserPost
from applications.user_wall.forms import UserPostForm


def fill_edit_post_form(
        form: UserPostForm | GroupPostForm,
        post: UserPost | GroupPost
) -> None:
    form.fields.get('title').widget.attrs.update({'value': post.title})
    form.fields.get('tags').widget.attrs.update({'value': form_tags_string(tags=post.tags)})
    form.fields.get('content').initial = post.content
    form.fields.get('draft').widget.attrs.update({'checked': not post.is_published})


def form_tags_string(tags: QuerySet[Tag]) -> str:
    tags_string = ''
    all_tags = tags.all()
    tags_number = len(all_tags) - 1
    for index, tag in enumerate(all_tags):
        if index == tags_number:
            tags_string += f'#{tag.title}'
        else:
            tags_string += f'#{tag.title}, '

    return tags_string


def calculate_post_page(
        paginate_by: int,
        author_id: int,
        model: ModelBase,
        post: UserPost | GroupPost,
        posts_to_show: str,
) -> int:
    """The function returns a number of the current page according to 'paginate_by' and 'posts_to_show' parameters."""
    if posts_to_show.lower() == 'published':
        posts = (
            model.objects.filter(author_id=author_id, is_published=True).
            order_by('-publication_date').values_list('pk', flat=True)
        )
    elif posts_to_show.lower() == 'unpublished':
        posts = (
            model.objects.filter(author_id=author_id, is_published=False).
            order_by('-publication_date').values_list('pk', flat=True)
        )
    else:
        posts = (
            model.objects.filter(author_id=author_id).
            order_by('-publication_date').values_list('pk', flat=True)
        )
    page = 0
    counter = 0
    for post_pk in posts:
        if counter % paginate_by == 0:
            page += 1
        if post_pk == post.pk:
            return page

        counter += 1

    return page
