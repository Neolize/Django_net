from datetime import date, datetime, timedelta

from django.core.handlers.wsgi import WSGIRequest

from applications.frontend.services.pagination import get_page_object
from applications.user_profiles.models import CustomUser
from applications.user_wall.services.crud.read import get_related_posts
from applications.user_wall.services.crud.update import update_user_posts_view_count
from applications.groups.services.crud.read import is_user_allowed_to_create_group


def get_min_birthdate() -> str:
    """Return min possible birthdate for user's birthday field"""
    min_year = date.today().year - 130
    return str(date(year=min_year, month=1, day=1))


def get_max_birthdate() -> str:
    """Return max possible birthdate for user's birthday field"""
    return str(date.today())


def form_user_profile_context_data(
        user_obj: CustomUser,
        request: WSGIRequest,
        paginate_by: int,
) -> dict:

    page = int(request.GET.get('page', 1))
    end = page * paginate_by
    start = end - paginate_by

    user_posts = get_related_posts(user=user_obj)

    page_obj = get_page_object(
        object_list=user_posts,
        paginate_by=paginate_by,
        page=page,
    )
    relevant_posts = user_posts[start:end]
    update_user_posts_view_count(
        user_pk=user_obj.pk,
        visitor_pk=request.user.pk,
        posts=relevant_posts,
    )
    today = datetime.today()
    return {
        'user_obj': user_obj,
        'posts_number': user_obj.user_posts.count(),
        'user_posts': relevant_posts,
        'followers': user_obj.followers.count(),
        'following': user_obj.owner.count(),
        'is_followed': is_followed(current_user=user_obj, visitor=request.user),
        'allowed_to_create_group': is_user_allowed_to_create_group(user_obj),
        'groups': user_obj.user_groups.all(),
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
        'is_owner': request.user.pk == user_obj.pk,
        'page_obj': page_obj,
    }


def is_followed(current_user: CustomUser, visitor: CustomUser) -> bool:
    if visitor.is_anonymous:
        return False
    return current_user.pk in visitor.owner.values_list('user__pk', flat=True)
