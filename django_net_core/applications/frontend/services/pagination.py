from django.core.paginator import Paginator, Page
from django.db.models import QuerySet


def get_page_object(
        object_list: QuerySet,
        paginate_by: int,
        page: int
) -> Page:
    paginator = Paginator(object_list, paginate_by)
    return paginator.get_page(page)


def get_posts_for_current_page(
        page: int,
        paginate_by: int,
        posts: QuerySet,
) -> QuerySet:

    end = page * paginate_by
    start = end - paginate_by

    return posts[start:end]
