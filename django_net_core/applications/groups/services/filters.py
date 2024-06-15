from django_filters.rest_framework import CharFilter, FilterSet, RangeFilter

from applications.groups import models


class GroupFilter(FilterSet):
    id = RangeFilter()
    title = CharFilter()

    class Meta:
        model = models.Group
        fields = ('id', 'title')
