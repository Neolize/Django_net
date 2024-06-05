from typing import Generator

from django.core.paginator import Paginator, Page
from django.db.models import QuerySet


def get_page_object(
        object_list: QuerySet | Generator,
        paginate_by: int,
        page: int
) -> Page:
    paginator = Paginator(object_list, paginate_by)
    return paginator.get_page(page)
