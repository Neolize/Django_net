from functools import wraps

from django.shortcuts import redirect
from django.http import HttpResponseForbidden, Http404
from django.core.handlers.wsgi import WSGIRequest

from applications.user_profiles.services.crud.read import get_user_for_profile
from applications.user_wall.services.crud.read import fetch_user_post, get_user_comment_by_pk
from applications.frontend.permissions import is_user_post_author, is_user_comment_author


FORBIDDEN_MESSAGE = """<div style=\"width: 700px; margin: auto; margin-top: 50px; font-size: 24px;\" >
            <h1 style=\"font-size: 44px;\"> Access forbidden!</h1> 
            <p>You don't have permission to access</p>
            </div>"""


class UserPermissionMixin:
    def has_permission(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)
        return super().dispatch(request, *args, **kwargs)


def check_user_request(func: callable):
    """Check if the request goes from an authenticated user and if user with given 'pk' exists."""
    @wraps(func)
    def wrapper(request: WSGIRequest, pk: int):
        if request.user.is_anonymous:
            return redirect(to='login')

        user_obj = get_user_for_profile(user_pk=pk)
        if not user_obj:
            raise Http404

        return func(request, pk, user_obj)

    return wrapper


def check_user_post_deletion_request(func: callable):
    """Check if the request goes from an authenticated user and if group with given 'group_slug' exists."""
    @wraps(func)
    def wrapper(request: WSGIRequest, user_post_slug: str):
        if request.user.is_anonymous:
            return redirect(to='login')

        user_post = fetch_user_post(user_post_slug)
        if not user_post:
            raise Http404

        if not is_user_post_author(visitor=request.user, post=user_post):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)

        return func(request, user_post)

    return wrapper


def check_user_comment_deletion_request(func: callable):
    """Check if the request goes from an authenticated user and if group comment with given 'comment_pk' exists."""
    @wraps(func)
    def wrapper(request: WSGIRequest, comment_pk: int):
        if request.user.is_anonymous:
            return redirect(to='login')

        comment = get_user_comment_by_pk(comment_pk)
        if not comment:
            raise Http404

        if not comment.author_id:
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)

        if not is_user_comment_author(visitor=request.user, comment=comment):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)

        return func(request, comment)

    return wrapper
