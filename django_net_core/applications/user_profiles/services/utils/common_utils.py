from datetime import date, datetime, timedelta

from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Page

from applications.abstract_activities.services.crud.update import update_posts_view_count
from applications.frontend.services.pagination import get_page_object
from applications.user_profiles.models import CustomUser
from applications.user_profiles.services.crud import read
from applications.user_wall.services.crud.read import get_related_posts
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
        posts_to_show: str,
) -> dict:

    page = int(request.GET.get('page', 1))
    is_owner = request.user.pk == user_obj.pk
    user_posts = get_related_posts(
        user=user_obj,
        owner=is_owner,
        posts_to_show=posts_to_show
    )
    page_obj = get_page_object(
        object_list=user_posts,
        paginate_by=paginate_by,
        page=page,
    )
    relevant_posts = page_obj.object_list

    update_posts_view_count(
        creator_pk=user_obj.pk,
        visitor_pk=request.user.pk,
        posts=relevant_posts,
    )
    return _collect_all_context_data(
        user_obj=user_obj,
        relevant_posts=relevant_posts,
        request=request,
        today=datetime.today(),
        is_owner=is_owner,
        page_obj=page_obj,
    )


def _collect_all_context_data(
        user_obj: CustomUser,
        relevant_posts: QuerySet,
        request: WSGIRequest,
        today: datetime,
        is_owner: bool,
        page_obj: Page,
) -> dict:

    published_posts_number = read.get_published_user_posts_number(user_obj)
    context_data = {
        'user_obj': user_obj,
        'published_posts_number': published_posts_number,
        'user_posts': relevant_posts,
        'followers': read.get_followers_number_from_user_obj(user_obj),
        'following': read.get_following_number_from_user_obj(user_obj),
        'is_followed': is_followed(current_user=user_obj, visitor=request.user),
        'allowed_to_create_group': is_user_allowed_to_create_group(user_obj),
        'groups': read.get_all_groups_from_user_obj(user_obj),
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
        'is_owner': is_owner,
        'page_obj': page_obj,
    }
    _include_unpublished_posts_number_to_context_data(
        owner=is_owner,
        data=context_data,
        user_obj=user_obj,
        published_posts_number=published_posts_number,
    )
    return context_data


def is_followed(current_user: CustomUser, visitor: CustomUser) -> bool:
    if visitor.is_anonymous:
        return False
    return current_user.pk in visitor.owner.values_list('user__pk', flat=True)


def _include_unpublished_posts_number_to_context_data(
        owner: bool,
        data: dict,
        user_obj: CustomUser,
        published_posts_number: int,
) -> None:
    """If owner visits the page and there's unpublished posts, they'll be added to the data dict."""
    all_posts_number = read.get_all_user_posts_number(user_obj)
    if owner:
        if all_posts_number > published_posts_number:
            data['unpublished_posts_number'] = all_posts_number - published_posts_number
        else:
            data['unpublished_posts_number'] = 0
