from datetime import datetime, timedelta

from applications.user_profiles.models import CustomUser
from applications.groups.models import Group
from applications.groups.services.crud.read import get_related_group_posts
from applications.groups.services.crud.update import update_group_posts_view_count


def is_user_subscribed_to_group(group: Group, visitor: CustomUser) -> bool:
    if visitor.is_anonymous:
        return False
    return group.pk in visitor.user_member.values_list('group__pk', flat=True)


def form_group_context_data(group: Group, user: CustomUser) -> dict:
    relevant_posts = get_related_group_posts(group)
    update_group_posts_view_count(
        group=group,
        visitor_pk=user.pk,
        posts=relevant_posts,
    )
    today = datetime.today()
    return {
        'group': group,
        'group_posts': relevant_posts,
        'is_subscribed_to_group': is_user_subscribed_to_group(
            group=group,
            visitor=user,
        ),
        'is_group_owner': group.creator.pk == user.pk,
        'post_number': 0,
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
        'page_obj': None,
    }
