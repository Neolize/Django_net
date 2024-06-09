from rest_framework import serializers

from applications.groups import models
from applications.user_wall.services.crud.crud_utils import return_unique_slug


class GroupDetailSerializer(serializers.ModelSerializer):
    """Serializer for group public API."""
    creator_id = serializers.SlugRelatedField(source='creator', slug_field='id', read_only=True)
    creator_name = serializers.SlugRelatedField(source='creator', slug_field='username', read_only=True)

    class Meta:
        model = models.Group
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'slug',
            'creator_id',
            'creator_name'
        )


class GroupCreationSerializer(serializers.ModelSerializer):
    """Serializer for group creation."""
    class Meta:
        model = models.Group
        fields = (
            'title',
            'description',
            'logo',
            'creator'
        )

    def create(self, validated_data):
        slug = return_unique_slug(
            str_for_slug=validated_data.get('title'),
            model=models.Group
        )
        validated_data['slug'] = slug
        return models.Group.objects.create(**validated_data)


class GroupEditingSerializer(serializers.ModelSerializer):
    """Serializer for group editing."""
    title = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = models.Group
        fields = (
            'title',
            'description',
            'logo'
        )

    def update(self, instance, validated_data):
        title = validated_data.get('title')
        if title and title != instance.title:
            # if new title was given, slug would be changed
            slug = return_unique_slug(
                str_for_slug=title,
                model=models.Group
            )
            instance.title = title
            instance.slug = slug

        instance.description = validated_data.get('description', instance.description)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance


class GroupDeletionSerializer(serializers.ModelSerializer):
    """Serializer for group deletion."""
    class Meta:
        model = models.Group
        fields = (
            'title',
            'description',
            'logo'
        )

    def delete(self, instance):
        return instance.delete()


class GroupListSerializer(serializers.ModelSerializer):
    """Public serializer for a list of groups."""
    class Meta:
        model = models.Group
        fields = (
            'id',
            'title',
            'slug'
        )


class CommentRecursiveSerializer(serializers.Serializer):
    """Display nested children comments."""
    def to_representation(self, instance):
        representation = self.parent.parent.__class__(instance, context=self.context)
        return representation.data


class FilterCommentListSerializer(serializers.ListSerializer):
    """Filter comments and leave on those which have parent_id as None."""
    def to_representation(self, instance):
        if not isinstance(instance, list):
            instance = instance.all()
        data = [comment for comment in instance if comment.parent is None]
        return super().to_representation(data=data)


class GroupPostCommentListSerializer(serializers.ModelSerializer):
    """Public serializer for a list of group comments."""
    author_id = serializers.SlugRelatedField(source='author', slug_field='id', read_only=True)
    author_name = serializers.SlugRelatedField(source='author', slug_field='username', read_only=True)
    children = CommentRecursiveSerializer(many=True)

    class Meta:
        model = models.GroupComment
        list_serializer_class = FilterCommentListSerializer
        fields = (
            'id',
            'content',
            'creation_date',
            'is_edited',
            'author_id',
            'author_name',
            'children'
        )


class GroupPostDetailSerializer(serializers.ModelSerializer):
    """Public serializer for a group post."""
    author_id = serializers.SlugRelatedField(source='author', slug_field='id', read_only=True)
    author_name = serializers.SlugRelatedField(source='author', slug_field='username', read_only=True)
    group_id = serializers.SlugRelatedField(source='group', slug_field='id', read_only=True)
    group_title = serializers.SlugRelatedField(source='group', slug_field='title', read_only=True)
    tags = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)
    comments = GroupPostCommentListSerializer(many=True)

    class Meta:
        model = models.GroupPost
        fields = (
            'id',
            'title',
            'publication_date',
            'last_edit',
            'view_counts',
            'slug',
            'group_id',
            'group_title',
            'tags',
            'author_id',
            'author_name',
            'comments'
        )
