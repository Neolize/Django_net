import pytest
from datetime import datetime

from applications.groups import models


@pytest.fixture
def new_group_factory(db):
    def create_group(
            title: str,
            description: str = 'description',
            logo: str = 'logo',
            creation_date: datetime = datetime(year=2024, month=1, day=1),
            slug: str = 'slug',
            creator_id: int = None
    ):
        group = models.Group.objects.create(
            title=title,
            description=description,
            logo=logo,
            creation_date=creation_date,
            slug=slug,
            creator_id=creator_id
        )
        return group
    return create_group


@pytest.fixture
def new_group(db, new_group_factory):
    return new_group_factory(title='First', slug='first')
