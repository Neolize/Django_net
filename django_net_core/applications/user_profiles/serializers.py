from rest_framework import serializers

from applications.user_profiles import models


class PrivateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = "__all__"


class PublicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'avatar',
            'last_login'
        )


class UserPersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPersonalData
        fields = "__all__"
