from datetime import datetime, timedelta

from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest

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
) -> dict:

    page = int(request.GET.get('page', 1))
    creator_pk = group.creator.pk
    group_posts = read.get_related_group_posts(group, owner=request.user.pk == creator_pk)

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
    )


def _collect_context_data(
        group: Group,
        relevant_posts: QuerySet,
        request: WSGIRequest,
        today: datetime,
        group_posts: QuerySet[GroupPost],
        paginate_by: int,
        page: int,
) -> dict:
    return {
        'group': group,
        'group_posts': relevant_posts,
        'is_subscribed_to_group': is_user_subscribed_to_group(
            group=group,
            visitor=request.user,
        ),
        'is_group_owner': group.creator.pk == request.user.pk,
        'posts_number': read.get_group_posts_number_from_group(group),
        'followers': read.get_group_members_number_from_group(group),
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
        'page_obj': get_page_object(
            object_list=group_posts,
            paginate_by=paginate_by,
            page=page,
        ),
    }
