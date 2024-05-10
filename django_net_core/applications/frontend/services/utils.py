from django.core.handlers.wsgi import WSGIRequest

from applications.abstract_activities.services.utils import get_previous_url
from applications.frontend.services import pagination
from applications.user_profiles.services.crud import read


def form_context_data_for_search_view(request: WSGIRequest, paginate_by: int) -> dict:
    user_input = request.GET.get('input')
    page = int(request.GET.get('page', 1))

    if user_input is None:
        users = read.get_all_users_with_personal_data()
    else:
        users = read.fetch_users_by_names(user_input)

    page_obj = pagination.get_page_object(
        object_list=users,
        paginate_by=paginate_by,
        page=page,
    )
    return {
        'users': page_obj.object_list,
        'previous_page': get_previous_url(request),
        'page_obj': page_obj,
    }
