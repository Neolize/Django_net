from applications.groups.models import GroupPost
from applications.user_profiles.models import CustomUser
from applications.user_wall.models import UserPost, UserComment


def is_user_post_author(visitor: CustomUser, post: UserPost | GroupPost) -> bool:
    return post.author_id == visitor.pk


def is_user_comment_author(visitor: CustomUser, comment: UserComment) -> bool:
    return comment.author_id == visitor.pk
