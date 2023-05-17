from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
# from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from applications.user_profiles import serializers
from applications.user_profiles.services.crud import read


class PublicCustomUserAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.PublicCustomUserSerializer
    queryset = read.get_all_users()


class PrivateCustomUserAPIViewSet(ModelViewSet):
    serializer_class = serializers.PrivateCustomUserSerializer
    queryset = read.get_all_users()
    permission_classes = (permissions.IsAuthenticated, )


class UserPersonalDataAPIViewSet(ModelViewSet):
    serializer_class = serializers.UserPersonalDataSerializer
    queryset = read.get_all_users_personal_data()
    permissions_class = (permissions.IsAuthenticated, )


# class GetCustomUserAPIView(RetrieveAPIView):
#     """Show user profile"""
#     queryset = read.get_all_users()
#     serializer_class = serializers.PublicCustomUserSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#
#
# class UpdateCustomUserAPIView(UpdateAPIView):
#     """Update user profile"""
#     serializer_class = serializers.PublicCustomUserSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#
#     def get_queryset(self):
#         return read.get_user_queryset_by_parameter(id=self.request.user.id)
