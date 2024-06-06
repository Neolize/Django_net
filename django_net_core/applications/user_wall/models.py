from django.db import models
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

from applications.abstract_activities import models as abstract_models


class Tag(models.Model):
    """Tag model for user's posts"""
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.title


class UserPost(abstract_models.AbstractPost):
    """User's post model"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_posts'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='user_posts')

    class Meta:
        db_table = 'post'

    def __str__(self):
        return f'{self.title} - {self.author}'


class UserComment(abstract_models.AbstractComment, MPTTModel):
    """User's comment model"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_comments'
    )
    post = models.ForeignKey('UserPost', on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    class MPTTMeta:
        """Sorting by nesting"""
        order_insertion_by = ('creation_date', )

    class Meta:
        db_table = 'user_comment'

    def __str__(self):
        return f'{self.author} - {self.post} - {self.content}'

    def delete(self, *args, **kwargs):
        if not UserComment.objects.filter(parent_id=self.pk).exists():
            return super().delete(*args, **kwargs)

        child_comments = list(UserComment.objects.filter(parent_id=self.pk))
        # make a list of out child comments in order not to lose them
        parent_pk = self.pk
        post_pk = self.post_id
        # assign 'parent_pk', 'post_pk' and 'child_comment' before deleting the comment
        # in order to save those parameters
        result = super().delete(*args, **kwargs)
        UserComment.objects.create(
            pk=parent_pk,
            content='This comment was deleted.',
            author_id=None,
            post_id=post_pk
        )
        for child in child_comments:
            child.parent_id = parent_pk
            child.save()

        return result
