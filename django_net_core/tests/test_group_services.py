import pytest

from applications.groups import models
from applications.groups.services.crud import read


@pytest.mark.django_db
def test_get_all_groups():
    groups = read.get_all_groups()
    assert groups.count() == 0

    models.Group.objects.create(title='Test', slug='test')
    groups = read.get_all_groups()
    assert groups.count() == 1


def test_get_group_by_slug(new_group):
    group = read.get_group_by_slug('first')
    assert group.title == 'First'

