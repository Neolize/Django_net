from django.core.handlers.wsgi import WSGIRequest

from applications.abstract_activities.services.utils import get_previous_url
from applications.frontend.services.pagination import get_page_object
from applications.user_profiles.services.crud.read import get_all_users_with_personal_data, fetch_users_by_names
from applications.groups.services.crud.read import get_all_groups, fetch_groups_by_titles


def form_context_data_for_people_search_view(request: WSGIRequest, paginate_by: int) -> dict:
    user_input = request.GET.get('input')
    page = int(request.GET.get('page', 1))

    if user_input is None:
        users = get_all_users_with_personal_data()
    else:
        users = fetch_users_by_names(user_input)

    page_obj = get_page_object(
        object_list=users,
        paginate_by=paginate_by,
        page=page,
    )
    return {
        'users': page_obj.object_list,
        'previous_page': get_previous_url(request),
        'page_obj': page_obj,
    }


def form_context_data_for_group_search_view(request: WSGIRequest, paginate_by: int) -> dict:
    user_input = request.GET.get('input')
    page = int(request.GET.get('page', 1))

    if user_input is None:
        groups = get_all_groups()
    else:
        groups = fetch_groups_by_titles(user_input)

    page_obj = get_page_object(
        object_list=groups,
        paginate_by=paginate_by,
        page=page,
    )
    return {
        'groups': page_obj.object_list,
        'previous_page': get_previous_url(request),
        'page_obj': page_obj,
    }
