from applications.abstract_activities.models import AbstractPost
from applications.user_profiles.models import CustomUser


def is_user_post_author(visitor: CustomUser, post: AbstractPost) -> bool:
    return post.author.pk == visitor.pk
