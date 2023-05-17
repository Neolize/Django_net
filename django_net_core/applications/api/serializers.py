from rest_framework import serializers

from applications.user_profiles import models


class CustomUserSerializer(serializers.ModelSerializer):
    pass


# from rest_framework import serializers
#
# from applications.user_profiles import models
#
#
# class PrivateCustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.CustomUser
#         fields = "__all__"
#
#
# class PublicCustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.CustomUser
#         fields = (
#             'username',
#             'first_name',
#             'last_name',
#             'middle_name',
#             'avatar',
#             'last_login'
#         )
#
#
# class UserPersonalDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.UserPersonalData
#         fields = "__all__"
#
#
# # from rest_framework import permissions
# # from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
# # # from rest_framework.generics import RetrieveAPIView, UpdateAPIView
# #
# # from applications.user_profiles import serializers
# # from applications.user_profiles.services.crud import read
# #
# #
# # class PublicCustomUserAPIViewSet(ReadOnlyModelViewSet):
# #     serializer_class = serializers.PublicCustomUserSerializer
# #     queryset = read.get_all_users()
# #
# #
# # class PrivateCustomUserAPIViewSet(ModelViewSet):
# #     serializer_class = serializers.PrivateCustomUserSerializer
# #     queryset = read.get_all_users()
# #     permission_classes = (permissions.IsAuthenticated, )
# #
# #
# # class UserPersonalDataAPIViewSet(ModelViewSet):
# #     serializer_class = serializers.UserPersonalDataSerializer
# #     queryset = read.get_all_users_personal_data()
# #     permissions_class = (permissions.IsAuthenticated, )
#
#
# # urlpatterns = [
# #     path("user/<int:pk>/", views.PublicCustomUserAPIViewSet.as_view({"get": "retrieve"})),
# #     path("user/private/<int:pk>/", views.PrivateCustomUserAPIViewSet.as_view({"get": "retrieve", "put": "update"})),
# #     path("user/personal-data/<int:pk>/", views.UserPersonalDataAPIViewSet.as_view({"get": "retrieve"})),
# # ]
