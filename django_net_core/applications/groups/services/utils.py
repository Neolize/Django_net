from datetime import datetime, timedelta

from applications.user_profiles.models import CustomUser
from applications.groups.models import Group
from applications.groups.services.crud import read


def is_user_subscribed_to_group(group: Group, visitor: CustomUser) -> bool:
    if visitor.is_anonymous:
        return False
    return group.pk in visitor.user_member.values_list('group__pk', flat=True)


def form_group_context_data(group: Group, user: CustomUser) -> dict:
    today = datetime.today()
    return {
        'group': group,
        'group_posts': read.get_related_group_posts(group),
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
