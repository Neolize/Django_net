from typing import Generator

from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, Page
from django.db.models import QuerySet


def get_page_object(
        object_list: QuerySet | Generator,
        paginate_by: int,
        page: int
) -> Page:
    paginator = Paginator(object_list, paginate_by)
    return paginator.get_page(page)


class GroupAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class GroupPostCommentAPIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class GroupPostAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GroupMemberAPIListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
