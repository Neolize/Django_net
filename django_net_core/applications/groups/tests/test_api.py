from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from applications.groups import models, serializers
from applications.user_profiles.models import CustomUser
from applications.groups.services.crud.read import get_all_groups_for_api_request


class GroupTestCase(APITestCase):
    def setUp(self):
        creator = CustomUser.objects.create(username='Test user', password='Test password')
        self.first_group = models.Group.objects.create(
            title='First test group',
            slug='first-test-group',
            creator_id=creator.pk
        )
        self.second_group = models.Group.objects.create(
            title='Second test group',
            slug='second-test-group',
            creator_id=creator.pk
        )
        self.third_group = models.Group.objects.create(
            title='Third test group',
            slug='third-test-group',
            creator_id=creator.pk
        )

    def test_group_list(self):
        groups = get_all_groups_for_api_request(creator_id=0)
        serializer = serializers.GroupListSerializer(groups, many=True)

        url = reverse('group_list_api')
        response = self.client.get(url)
        response_data = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response_data)

    def test_group_filter(self):
        url = reverse('group_list_api')
        response = self.client.get(url, data={'id_min': self.third_group.pk})

        group = get_all_groups_for_api_request(creator_id=0)[2]
        data = serializers.GroupListSerializer(group).data
        response_data = response.data.get('results')[0]

        self.assertEqual(response_data, data)
