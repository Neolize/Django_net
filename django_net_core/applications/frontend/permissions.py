from django.contrib.auth import logout
from rest_framework.permissions import BasePermission

from applications.groups.models import GroupPost, GroupComment
from applications.groups.services.crud.read import get_group_by_slug
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


class IsGroupCreator(BasePermission):
    """Allows access only to a group creator."""
    def has_permission(self, request, view):
        group = get_group_by_slug(view.kwargs.get('group_slug', ''))
        if not group:
            return False
        return group.creator_id == request.user.pk
