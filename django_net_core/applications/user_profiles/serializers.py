from rest_framework import serializers

from applications.user_profiles import models


class PrivateCustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(write_only=True)

    class Meta:
        model = models.CustomUser
        exclude = (
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )


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
