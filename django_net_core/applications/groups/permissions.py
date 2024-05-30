from functools import wraps

from django.shortcuts import redirect
from django.http import Http404, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest

from applications.user_profiles.models import CustomUser
from applications.user_profiles.permissions import FORBIDDEN_MESSAGE
from applications.groups.models import Group
from applications.groups.services.crud.read import get_group_by_slug, fetch_group_post, get_group_comment_by_pk
from applications.frontend.permissions import is_user_post_author, is_user_comment_author


GROUP_FORBIDDEN_MESSAGE = """<div style=\"width: 700px; margin: auto; margin-top: 50px; font-size: 24px;\" >
            <h1 style=\"font-size: 44px;\"> Access forbidden!</h1> 
            <p>You already have a group</p>
            </div>"""

GROUP_CREATION_FORBIDDEN_MESSAGE = """<div style=\"width: 700px; margin: auto; margin-top: 50px; font-size: 24px;\" >
            <h1 style=\"font-size: 44px;\"> Access forbidden!</h1> 
            <p>Only group author can create a new post.</p>
            </div>"""


def is_user_group_author(visitor: CustomUser, group: Group) -> bool:
    return group.creator.pk == visitor.pk


def check_group_request(func: callable):
    """Check request for group views."""
    @wraps(func)
    def wrapper(request: WSGIRequest, group_slug: str):
        if request.user.is_anonymous:
            return redirect(to='login')

        group = get_group_by_slug(group_slug)
        if not group:
            raise Http404

        return func(request, group_slug, group)

    return wrapper


def check_group_post_deletion_request(func: callable):
    """Check request for 'delete_group_post' view."""
    @wraps(func)
    def wrapper(request: WSGIRequest, group_post_slug: str):
        if request.user.is_anonymous:
            return redirect(to='login')

        group_post = fetch_group_post(group_post_slug)
        if not group_post:
            raise Http404

        if not is_user_post_author(visitor=request.user, post=group_post):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)

        return func(request, group_post)

    return wrapper


def check_group_comment_deletion_request(func: callable):
    """Check request for 'delete_group_comment' view."""
    @wraps(func)
    def wrapper(request: WSGIRequest, comment_pk: int):
        if request.user.is_anonymous:
            return redirect(to='login')

        comment = get_group_comment_by_pk(comment_pk)
        if not comment:
            raise Http404

        if not is_user_comment_author(visitor=request.user, comment=comment):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)

        return func(request, comment)

    return wrapper
