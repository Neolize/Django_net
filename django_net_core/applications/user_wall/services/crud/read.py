from django.db.models import QuerySet

from applications.user_wall import models


def get_user_posts(user_pk) -> QuerySet[models.UserPost]:
    # return models.UserPost.objects.filter(author_id=user_pk).prefetch_related('tags')
    return models.UserPost.objects.filter(author_id=user_pk)

#  posts = models.UserPost.objects.filter(author_id=6, is_published=True).
#  values('title', 'content', 'publication_date', 'last_edit', 'view_counts', 'tags__title')

# def get_user_posts(user_pk) -> QuerySet[models.UserPost]:
#     values = (
#         'title',
#         'content',
#         'publication_date'
#         'last_edit',
#         'view_counts',
#     )
#     return models.UserPost.objects.filter(author_id=user_pk, is_published=True).values(*values)
# { %
# for tag in post.tags.all %}
# < span > {{tag.title}} < / span >
# { % endfor %}
