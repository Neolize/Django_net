from rest_framework import serializers

from applications.user_profiles import models


class PublicUserDetailSerializer(serializers.ModelSerializer):
    """User's serializer for public API."""
    class Meta:
        model = models.CustomUser
        fields = (
            'username',
            'email',
            'date_joined',
            'last_login',
            'gender'
        )


class PublicUserListSerializer(serializers.ModelSerializer):
    """List of users serializer for public API."""
    class Meta:
        model = models.CustomUser
        fields = (
            'username',
            'email'
        )
