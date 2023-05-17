from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from applications.user_profiles import serializers
from applications.user_profiles.services.crud import read


class PublicCustomUserAPIViewSet(ModelViewSet):
    serializer_class = serializers.PublicCustomUserSerializer
    queryset = read.get_all_users()
    permission_classes = (permissions.IsAuthenticated, )


class PrivateCustomUserAPIViewSet(ModelViewSet):
    serializer_class = serializers.PrivateCustomUserSerializer
    queryset = read.get_all_users()
    permission_classes = (permissions.IsAdminUser, )

