from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from applications.groups import models, serializers
from applications.user_profiles.models import CustomUser
from applications.groups.services.crud.read import get_all_groups_for_api_request


class GroupTestCase(APITestCase):
    def test_group_list(self):
        creator = CustomUser.objects.create(username='Test user', password='Test password')
        models.Group.objects.create(
            title='First test group',
            slug='first-test-group',
            creator_id=creator.pk
        )
        models.Group.objects.create(
            title='Second test group',
            slug='second-test-group',
            creator_id=creator.pk
        )
        groups = get_all_groups_for_api_request(creator_id=0)
        serializer = serializers.GroupListSerializer(groups, many=True)

        url = reverse('group_list_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data.get('results'))
