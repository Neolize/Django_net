from rest_framework import serializers

from applications.groups import models


class PublicGroupDetailSerializer(serializers.ModelSerializer):
    """Serializer for group public API."""
    creator_id = serializers.SlugRelatedField(source='creator', slug_field='id', read_only=True)
    creator_name = serializers.SlugRelatedField(source='creator', slug_field='username', read_only=True)

    class Meta:
        model = models.Group
        exclude = (
            'logo',
            'creator'
        )


class PublicGroupListSerializer(serializers.ModelSerializer):
    """Public serializer for a list of groups."""
    class Meta:
        model = models.Group
        fields = (
            'title',
            'slug'
        )


class PublicGroupPostDetailSerializer(serializers.ModelSerializer):
    """Public serializer for a group post."""
    author_id = serializers.SlugRelatedField(source='author', slug_field='id', read_only=True)
    author_name = serializers.SlugRelatedField(source='author', slug_field='username', read_only=True)
    group_id = serializers.SlugRelatedField(source='group', slug_field='id', read_only=True)
    group_title = serializers.SlugRelatedField(source='group', slug_field='title', read_only=True)
    tags = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)

    class Meta:
        model = models.GroupPost
        exclude = (
            'content',
            'user_list',
            'is_published',
            'author',
            'group'
        )
