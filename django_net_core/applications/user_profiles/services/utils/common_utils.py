from datetime import date, datetime

from django.core.handlers.wsgi import WSGIRequest

from applications.user_profiles.models import CustomUser
from applications.user_wall.services.crud.read import get_user_posts
from applications.frontend.services.pagination import get_page_object

from applications.user_wall.services.crud.update import update_user_posts_view_counts


def get_min_birthdate() -> str:
    """Return min possible birthdate for user's birthday field"""
    min_year = date.today().year - 130
    return str(date(year=min_year, month=1, day=1))


def get_max_birthdate() -> str:
    """Return max possible birthdate for user's birthday field"""
    return str(date.today())


def form_user_profile_context_data(
        user_obj: CustomUser,
        pk: int,
        request: WSGIRequest,
        paginate_by: int,
) -> dict:

    today = datetime.today()

    page = int(request.GET.get('page', 1))
    end = page * paginate_by
    start = end - paginate_by

    user_posts = get_user_posts(user_pk=pk)

    page_obj = get_page_object(
        object_list=user_posts,
        paginate_by=paginate_by,
        page=page,
    )

    update_user_posts_view_counts(
        user=user_obj,
        visitor_pk=request.user.pk,
        start=start,
        end=end,
    )

    return {
        'user_obj': user_obj,
        'user_posts': user_posts[start:end],
        'today_date': today.date(),
        'yesterday_date': datetime(year=today.year, month=today.month, day=today.day - 1).date(),
        'is_owner': request.user.pk == pk,
        'page_obj': page_obj,
    }
