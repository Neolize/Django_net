from django.contrib.auth import logout

from applications.groups.models import GroupPost, GroupComment
from applications.user_profiles.models import CustomUser
from applications.user_wall.models import UserPost, UserComment


def is_user_post_author(visitor: CustomUser, post: UserPost | GroupPost) -> bool:
    return post.author_id == visitor.pk


def is_user_comment_author(visitor: CustomUser, comment: UserComment | GroupComment) -> bool:
    return comment.author_id == visitor.pk


class UnauthenticatedPermissionsMixin:
    def has_permissions(self):
        return not self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            logout(request)     # log out users if they try to open login or signup page while being logged in
        return super().dispatch(request, *args, **kwargs)
