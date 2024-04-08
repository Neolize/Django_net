from datetime import datetime, timedelta

from django.core.handlers.wsgi import WSGIRequest

from applications.frontend.services.pagination import get_page_object, get_posts_for_current_page
from applications.user_profiles.models import CustomUser
from applications.groups.models import Group
from applications.groups.services.crud.read import get_related_group_posts
from applications.groups.services.crud.update import update_group_posts_view_count


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
    group_posts = get_related_group_posts(group)

    relevant_posts = get_posts_for_current_page(
        page=page,
        paginate_by=paginate_by,
        posts=group_posts,
    )
    update_group_posts_view_count(
        group=group,
        visitor_pk=request.user.pk,
        posts=relevant_posts,
    )
    today = datetime.today()
    return {
        'group': group,
        'group_posts': relevant_posts,
        'is_subscribed_to_group': is_user_subscribed_to_group(
            group=group,
            visitor=request.user,
        ),
        'is_group_owner': group.creator.pk == request.user.pk,
        'posts_number': group.group_posts.count(),
        'followers': group.group_members.count(),
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
        'page_obj': get_page_object(
            object_list=group_posts,
            paginate_by=paginate_by,
            page=page,
        ),
    }
