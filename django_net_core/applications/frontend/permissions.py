from applications.groups.models import GroupPost
from applications.user_profiles.models import CustomUser
from applications.user_wall.models import UserPost


def is_user_post_author(visitor: CustomUser, post: UserPost | GroupPost) -> bool:
    return post.author.pk == visitor.pk
