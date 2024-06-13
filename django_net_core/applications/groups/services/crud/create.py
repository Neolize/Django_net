import logging
from datetime import date

from django.core.handlers.wsgi import WSGIRequest
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.request import Request
from rest_framework.serializers import SerializerMetaclass, ModelSerializer

from applications.groups import models, forms
from applications.groups.services.crud.read import is_user_allowed_to_create_group
from applications.user_profiles.models import CustomUser
from applications.user_wall.services.crud import crud_utils
from applications.user_wall.services.crud.create import return_tag_objects_from_list, add_tags_to_post
from applications.abstract_activities.services.crud.create import create_comment, is_new_comment_valid


LOGGER = logging.getLogger('main_logger')


def create_new_group_from_form_data(data: dict, data_files: dict, user_pk: int) -> models.Group | bool:
    return _create_new_group(
        title=data.get('title'),
        description=data.get('description'),
        logo=data_files.get('logo'),
        creator_id=user_pk,
    )


def _create_new_group(
        title: str,
        description: str,
        logo: InMemoryUploadedFile,
        creator_id: int,
) -> models.Group | bool:
    slug = crud_utils.return_unique_slug(str_for_slug=title, model=models.Group)

    try:
        new_group = models.Group.objects.create(
            title=title,
            description=description,
            logo=logo,
            creation_date=date.today(),
            slug=slug,
            creator_id=creator_id,
        )
    except Exception as exc:
        LOGGER.error(exc)
        new_group = False

    return new_group


def create_new_group_follower(group: models.Group, member: CustomUser) -> None:
    try:
        models.GroupMember.objects.create(
            member=member,
            group=group,
        )
    except Exception as exc:
        LOGGER.error(exc)


def create_group_post_from_form_data(
        data: dict,
        user_pk: int,
        group_pk: int,
) -> bool:
    is_published = not data.get('draft')
    return _create_group_post(
        title=data.get('title'),
        content=data.get('content'),
        tags=data.get('tags'),
        is_published=is_published,
        author_id=user_pk,
        group_id=group_pk,
    )


def _create_group_post(
        title: str,
        content: str,
        tags: str,
        is_published: bool,
        author_id: int,
        group_id: int,
) -> bool:

    slug = crud_utils.return_unique_slug(str_for_slug=title, model=models.GroupPost)
    try:
        new_group_post = models.GroupPost.objects.create(
            title=title,
            content=content,
            slug=slug,
            is_published=is_published,
            author_id=author_id,
            group_id=group_id,
        )
        tags = return_tag_objects_from_list(
            crud_utils.form_tag_list(tags)
        )
        add_tags_to_post(tags=tags, post=new_group_post)
        is_created = True
    except Exception as exc:
        LOGGER.error(exc)
        is_created = False

    return is_created


def create_comment_for_group_post(
        form: forms.GroupCommentForm,
        request: WSGIRequest,
) -> bool:

    content = form.cleaned_data.get('comment', '')
    post_id = int(request.POST.get('post_id'))
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
        model=models.GroupComment,
    )
    if not is_created:
        form.add_error(None, 'An error occurred during a comment creation. Try one more time.')

    return is_created


def create_new_group_from_api_request(
        request: Request,
        serializer: SerializerMetaclass
) -> ModelSerializer | bool:
    if not is_user_allowed_to_create_group(request.user):
        return False

    request.data['creator'] = request.user.pk
    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


def create_group_post_from_api_request(
        request: Request,
        serializer: SerializerMetaclass,
        group_id: int
) -> ModelSerializer | bool:

    request.data['author'] = request.user.pk
    request.data['group'] = group_id

    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer
