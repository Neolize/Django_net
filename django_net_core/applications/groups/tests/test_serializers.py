from django.test import TestCase

from applications.groups import serializers, models
from applications.groups.services.crud.read import get_all_groups_for_api_request
from applications.user_profiles.models import CustomUser


class GroupListSerializerTestCase(TestCase):
    def test_get(self):
        creator = CustomUser.objects.create(username='Test user', password='Test password')
        group_a = models.Group.objects.create(
            title='First test group',
            slug='first-test-group',
            creator_id=creator.pk
        )
        group_b = models.Group.objects.create(
            title='Second test group',
            slug='second-test-group',
            creator_id=creator.pk
        )
        groups = get_all_groups_for_api_request(creator_id=0)
        data = serializers.GroupListSerializer(groups, many=True).data
        expected_data = [
            {
                'id': group_a.pk,
                'title': 'First test group',
                'slug': 'first-test-group',
                'is_creator': False
            },
            {
                'id': group_b.pk,
                'title': 'Second test group',
                'slug': 'second-test-group',
                'is_creator': False
            }
        ]
        self.assertEqual(data, expected_data)
