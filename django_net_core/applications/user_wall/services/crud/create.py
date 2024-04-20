import logging

from django.core.handlers.wsgi import WSGIRequest
from django.db.utils import DataError

from applications.abstract_activities.services.crud.create import create_comment, is_new_comment_valid

from applications.groups.models import GroupPost

from applications.user_wall import models, forms
from applications.user_wall.services.crud import crud_utils
from applications.user_wall.services.crud.read import get_tag_by_title

LOGGER = logging.getLogger('main_logger')


def create_user_post_from_form_data(data: dict, user_pk: int) -> bool:
    is_published = not data.get('draft')
    return _create_user_post(
        title=data.get('title'),
        content=data.get('content'),
        tags=data.get('tags'),
        user_pk=user_pk,
        is_published=is_published,
    )


def _create_user_post(
        title: str,
        content: str,
        user_pk: int,
        is_published: bool,
        tags: str,
) -> bool:

    slug = crud_utils.return_unique_slug(str_for_slug=title, model=models.UserPost)

    try:
        new_post = models.UserPost.objects.create(
            title=title,
            content=content,
            slug=slug,
            is_published=is_published,
            author_id=user_pk,
        )
        tags = return_tag_objects_from_list(
            crud_utils.form_tag_list(tags)
        )
        add_tags_to_post(tags=tags, post=new_post)
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created


def _create_new_tag(new_tag: str) -> models.Tag | bool:
    created_tag = False

    if not models.Tag.objects.filter(title__iexact=new_tag).exists():
        slug = crud_utils.return_unique_slug(str_for_slug=new_tag, model=models.Tag)

        try:
            created_tag = models.Tag.objects.create(title=new_tag.lower(), slug=slug)
        except DataError as exc:
            LOGGER.error(exc)
            created_tag = False

    return created_tag


def add_tags_to_post(tags: list[models.Tag], post: models.UserPost | GroupPost) -> None:
    for tag in tags:
        post.tags.add(tag)


def create_comment_for_user_post(
        form: forms.UserCommentForm,
        request: WSGIRequest,
) -> bool:

    content = form.cleaned_data.get('comment', '')
    post_id = int(request.POST.get('post_id', 0))
    parent_id = int(request.POST.get('parent_id')) if request.POST.get('parent_id') else None

    if not is_new_comment_valid(
        content=content,
        form=form,
        user=request.user,
        parent_pk=parent_id,
    ):
        return False

    is_created = create_comment(
        content=content,
        author_id=request.user.pk,
        post_id=post_id,
        parent_id=parent_id,
        model=models.UserComment,
    )
    if not is_created:
        form.add_error(None, 'An error occurred during a comment creation. Try one more time.')

    return is_created


def return_tag_objects_from_list(tag_list: list[str]) -> list[models.Tag]:
    """If there's no tag with a given title, a new tag will be created. Otherwise, existing one will be extracted."""
    tags = []
    for tag in tag_list:
        created_tag = _create_new_tag(tag)
        if created_tag:
            tags.append(created_tag)
        elif new_tag := get_tag_by_title(tag=tag):
            tags.append(new_tag)

    return tags
