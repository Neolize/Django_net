from datetime import datetime, timedelta

from django.core.handlers.wsgi import WSGIRequest

from applications.abstract_activities.services.utils import get_previous_url
from applications.frontend.services.pagination import get_page_object
from applications.user_wall.services.crud import read as uw_read
from applications.user_profiles.services.crud import read as up_read
from applications.groups.services.crud import read as g_read


def form_context_data_for_people_search_view(request: WSGIRequest, paginate_by: int) -> dict:
    user_input = request.GET.get('input')
    page = int(request.GET.get('page', 1))

    if user_input is None:
        users = up_read.get_all_users_with_personal_data()
    else:
        users = up_read.fetch_users_by_names(user_input)

    page_obj = get_page_object(
        object_list=users,
        paginate_by=paginate_by,
        page=page,
    )
    return {
        'users': page_obj.object_list,
        'previous_page': get_previous_url(request),
        'page_obj': page_obj
    }


def form_context_data_for_group_search_view(request: WSGIRequest, paginate_by: int) -> dict:
    user_input = request.GET.get('input')
    page = int(request.GET.get('page', 1))

    if user_input is None:
        groups = g_read.get_all_groups()
    else:
        groups = g_read.fetch_groups_by_titles(user_input)

    page_obj = get_page_object(
        object_list=groups,
        paginate_by=paginate_by,
        page=page,
    )
    return {
        'groups': page_obj.object_list,
        'previous_page': get_previous_url(request),
        'page_obj': page_obj
    }


def form_context_data_for_posts_search_view(request: WSGIRequest, paginate_by: int) -> dict:
    user_input = request.GET.get('input')
    page = int(request.GET.get('page', 1))

    if user_input is None:
        group_posts = g_read.get_all_posts_from_all_groups()
        user_posts = uw_read.get_all_posts_from_all_users()
    else:
        group_posts = g_read.select_posts_from_all_groups_by_user_input(user_input)
        user_posts = uw_read.select_posts_from_all_users_by_user_input(user_input)

    posts = list(group_posts) + list(user_posts)
    page_obj = get_page_object(
        object_list=posts,
        paginate_by=paginate_by,
        page=page
    )
    today = datetime.today()
    return {
        'posts': page_obj.object_list,
        'previous_page': get_previous_url(request),
        'page_obj': page_obj,
        'today_date': today.date(),
        'yesterday_date': (today - timedelta(days=1)).date(),
    }
