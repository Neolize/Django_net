import re

from django.db.models import QuerySet
from django.db.models.base import ModelBase
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.handlers.wsgi import WSGIRequest

from applications.groups.models import GroupPost, GroupComment
from applications.groups.forms import GroupPostForm, GroupCommentForm
from applications.groups.services.crud.read import get_group_comment_by_pk

from applications.user_wall.models import Tag, UserPost, UserComment
from applications.user_wall.forms import UserPostForm, UserCommentForm
from applications.user_wall.services.crud.read import get_user_comment_by_pk


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


def get_parent_comment(parent_pk: int, form: GroupCommentForm | UserCommentForm) -> GroupComment | UserComment | bool:
    """The function will return a user's parent comment or a group parent comment depending on
     an instance of the given comment"""
    if isinstance(form, UserCommentForm):
        parent_comment = get_user_comment_by_pk(parent_pk)
    else:
        parent_comment = get_group_comment_by_pk(parent_pk)

    return parent_comment


def get_previous_url(request: WSGIRequest):
    """Return the previous user's url"""
    previous_url = request.META.get('HTTP_REFERER')
    if not url_has_allowed_host_and_scheme(url=previous_url, allowed_hosts=request.get_host()):
        previous_url = 'home'
    return previous_url


def fetch_page_from_request(request: WSGIRequest) -> int:
    """Return the page number from the gotten request."""
    if request.method.lower() == 'get':
        return int(request.GET.get('page', 0))
    return fetch_page_from_previous_url(request)


def fetch_posts_to_show_from_previous_url(request: WSGIRequest) -> str:
    """Retrieve 'posts_to_show' parameter from the gotten request using previous url."""
    url = get_previous_url(request)
    match = re.findall(r'posts=([^&]+)', url)
    if match:
        return match[-1]
    return ''


def fetch_page_from_previous_url(request: WSGIRequest) -> int:
    """Retrieve the page number from the gotten request using previous url."""
    url = get_previous_url(request)
    match = re.findall(r'page=([^&]+)', url)
    if match and match[-1].isdigit():
        return int(match[-1])   # there can be several 'page' parameters: ?page=1&page=2&page=3
    return 0
