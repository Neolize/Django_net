import pytest

from applications.groups import models
from applications.groups.services.crud import read


@pytest.mark.django_db
def test_count_groups():
    groups = read.get_all_groups()
    assert groups.count() == 0

    models.Group.objects.create(title='Test', slug='test')
    groups = read.get_all_groups()
    assert groups.count() == 1

