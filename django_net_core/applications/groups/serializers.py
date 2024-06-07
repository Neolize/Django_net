from rest_framework import serializers

from applications.groups import models
from applications.user_wall.services.crud.crud_utils import return_unique_slug


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


class CommentRecursiveSerializer(serializers.Serializer):
    """Display nested children comments."""
    def to_representation(self, instance):
        representation = self.parent.parent.__class__(instance, context=self.context)
        return representation.data


class FilterCommentListSerializer(serializers.ListSerializer):
    """Filter comments and leave on those which have parent_id as None."""
    def to_representation(self, instance):
        data = [comment for comment in instance.all() if comment.parent is None]
        return super().to_representation(data=data)


class PublicGroupPostCommentListSerializer(serializers.ModelSerializer):
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


class PublicGroupPostDetailSerializer(serializers.ModelSerializer):
    """Public serializer for a group post."""
    author_id = serializers.SlugRelatedField(source='author', slug_field='id', read_only=True)
    author_name = serializers.SlugRelatedField(source='author', slug_field='username', read_only=True)
    group_id = serializers.SlugRelatedField(source='group', slug_field='id', read_only=True)
    group_title = serializers.SlugRelatedField(source='group', slug_field='title', read_only=True)
    tags = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)
    comments = PublicGroupPostCommentListSerializer(many=True)

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


class GroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, allow_blank=True)
    logo = serializers.ImageField(allow_null=True, allow_empty_file=True)
    creator_id = serializers.IntegerField()
    slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        slug = return_unique_slug(
            str_for_slug=validated_data.get('title'),
            model=models.Group
        )
        validated_data['slug'] = slug
        return models.Group.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('title') != instance.title:
            instance.title = validated_data.get('title')
            slug = return_unique_slug(
                str_for_slug=instance.title,
                model=models.Group
            )
            instance.slug = slug

        instance.description = validated_data.get('description', instance.description)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.creator_id = validated_data.get('creator_id', instance.creator_id)

        instance.save()
        return instance

    def delete(self, instance):
        return instance.delete()
