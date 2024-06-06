from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

from mptt.models import MPTTModel, TreeForeignKey

from applications.abstract_activities import models as abstract_models
from applications.user_wall.models import Tag


class Group(models.Model):
    """User's group."""
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=1000, blank=True)
    logo = models.ImageField(upload_to='group/logo/%Y/%m/%d/', blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=125, blank=True, unique=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_groups'
    )

    class Meta:
        db_table = 'group'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('group', kwargs={'group_slug': self.slug})

    def get_absolute_url_for_post_creation(self):
        return reverse_lazy('create_group_post', kwargs={'group_slug': self.slug})

    def get_absolute_url_for_followers(self):
        return reverse_lazy('group_followers', kwargs={'group_slug': self.slug})


class GroupMember(models.Model):
    """Group member model."""
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_member'
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='group_members')

    class Meta:
        db_table = 'group_member'

    def __str__(self):
        return f'Group: {self.group} - member: {self.member}'


class GroupPost(abstract_models.AbstractPost):
    """Group's Post model."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='group_posts'
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='group_posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='group_posts')

    class Meta:
        db_table = 'group_post'

    def __str__(self):
        return self.title


class GroupComment(abstract_models.AbstractComment, MPTTModel):
    """Group's Comment model."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='group_comments'
    )
    post = models.ForeignKey('GroupPost', on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    class MPTTMeta:
        """Sorting by nesting."""
        order_insertion_by = ('creation_date', )

    class Meta:
        db_table = 'group_comment'

    def __str__(self):
        return f'{self.author} - {self.post} - {self.content}'

    def delete(self, *args, **kwargs):
        if not GroupComment.objects.filter(parent_id=self.pk).exists():
            return super().delete(*args, **kwargs)

        child_comments = list(GroupComment.objects.filter(parent_id=self.pk))
        # make a list of out child comments in order not to lose them
        parent_pk = self.pk
        post_pk = self.post_id
        # assign 'parent_pk', 'post_pk' and 'child_comment' before deleting the comment
        # in order to save those parameters
        result = super().delete(*args, **kwargs)
        GroupComment.objects.create(
            pk=parent_pk,
            content='This comment was deleted.',
            author_id=None,
            post_id=post_pk
        )
        for child in child_comments:
            child.parent_id = parent_pk
            child.save()

        return result
