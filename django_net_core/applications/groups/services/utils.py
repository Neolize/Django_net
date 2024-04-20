from datetime import datetime, timedelta

from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest

from django_net_core.settings import GROUP_POSTS_PAGINATE_BY
from applications.abstract_activities.services.utils import calculate_post_page
from applications.abstract_activities.services.crud.update import update_posts_view_count
from applications.frontend.services.pagination import get_page_object, get_posts_for_current_page
from applications.user_profiles.models import CustomUser
from applications.groups.models import Group, GroupPost
from applications.groups.services.crud import read


def is_user_subscribed_to_group(group: Group, visitor: CustomUser) -> bool:
    if visitor.is_anonymous:
        return False
    return group.pk in visitor.user_member.values_list('group__pk', flat=True)


def form_group_context_data(
        group: Group,
        request: WSGIRequest,
        paginate_by: int,
        posts_to_show: str,
) -> dict:

    page = int(request.GET.get('page', 1))
    creator_pk = group.creator.pk
    is_owner = request.user.pk == creator_pk

    group_posts = read.get_related_group_posts(
        group,
        owner=is_owner,
        posts_to_show=posts_to_show,
    )

    relevant_posts = get_posts_for_current_page(
        page=page,
        paginate_by=paginate_by,
        posts=group_posts,
    )
    update_posts_view_count(
        creator_pk=creator_pk,
        visitor_pk=request.user.pk,
        posts=relevant_posts,
    )
    return _collect_context_data(
        group=group,
        relevant_posts=relevant_posts,
        request=request,
        today=datetime.today(),
        group_posts=group_posts,
        paginate_by=paginate_by,
        page=page,
        owner=is_owner,
    )


def _collect_context_data(
        group: Group,
        relevant_posts: QuerySet,
        request: WSGIRequest,
        today: datetime,
        group_posts: QuerySet[GroupPost],
        paginate_by: int,
        page: int,
        owner: bool,
) -> dict:
    published_posts_number = read.get_published_group_posts_number(group)
    context_data = {
        'group': group,
        'group_posts': relevant_posts,
        'is_subscribed_to_group': is_user_subscribed_to_group(
            group=group,
            visitor=request.user,
        ),
        'is_group_owner': group.creator.pk == request.user.pk,
        # 'posts_number': read.get_group_posts_number_from_group(group=group, owner=owner),
        'published_posts_number': published_posts_number,
        'followers': read.get_group_members_number_from_group(group),
        'is_owner': owner,
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
        'page_obj': get_page_object(
            object_list=group_posts,
            paginate_by=paginate_by,
            page=page,
        ),
    }
    _include_unpublished_group_posts_number_to_context_data(
        data=context_data,
        owner=owner,
        group=group,
        published_posts_number=published_posts_number,
    )
    return context_data


def _include_unpublished_group_posts_number_to_context_data(
        data: dict,
        owner: bool,
        published_posts_number: int,
        group: Group,
) -> None:
    """If group creator visits the page and there's unpublished posts, they'll be added to the data dict."""
    all_posts_number = read.get_all_group_posts_number(group)
    if owner:
        if all_posts_number > published_posts_number:
            data['unpublished_posts_number'] = all_posts_number - published_posts_number
        else:
            data['unpublished_posts_number'] = 0


def redirect_to_the_current_group_post_page(request: WSGIRequest, group: Group) -> HttpResponseRedirect:
    # visitors can see only published posts
    posts_to_show = request.POST.get('posts', '') if request.user.pk == group.creator_id else 'published'

    base_url = reverse('group', kwargs={'group_slug': group.slug})
    page = _calculate_post_page_from_group_comment(
        request=request,
        group=group,
        posts_to_show=posts_to_show,
    )
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')


def _calculate_post_page_from_group_comment(
        request: WSGIRequest,
        group: Group,
        posts_to_show: str,
) -> int:
    """The function calculates and returns a number of the current page according to parameters in request."""
    post_id = int(request.POST.get('post_id', 0))
    post = read.get_group_post_by_pk(post_pk=post_id)
    if not post:
        return 1    # if post with given 'pk' does not exist, the function will return the first page number.

    return calculate_post_page(
        paginate_by=GROUP_POSTS_PAGINATE_BY,
        author_id=group.creator_id,
        model=GroupPost,
        post=post,
        posts_to_show=posts_to_show,
    )


def add_new_params_to_request_from_group_comment(request: WSGIRequest, group: Group) -> None:
    # visitors can see only published posts
    posts_to_show = request.POST.get('posts', '') if request.user.pk == group.creator_id else 'published'
    page = _calculate_post_page_from_group_comment(
        request=request,
        group=group,
        posts_to_show=posts_to_show,
    )
    request.GET._mutable = True
    request.GET['page'] = page
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to the request
        request.GET['posts'] = posts_to_show
