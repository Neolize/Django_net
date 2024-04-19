from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect

from django_net_core.settings import USER_POSTS_PAGINATE_BY
from applications.abstract_activities.services.utils import calculate_post_page
from applications.user_profiles.models import CustomUser
from applications.user_wall.models import UserPost
from applications.user_wall.services.crud.read import get_user_post_by_pk


def redirect_to_the_current_post_page(request: WSGIRequest, user_obj: CustomUser) -> HttpResponseRedirect:
    # visitors can see only published posts
    posts_to_show = request.POST.get('posts', '') if request.user.pk == user_obj.pk else 'published'

    base_url = reverse('user_profile', kwargs={'pk': user_obj.pk})
    page = _calculate_post_page_from_user_comment(
        request=request,
        user_obj=user_obj,
        posts_to_show=posts_to_show,
    )
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')


def _calculate_post_page_from_user_comment(
        request: WSGIRequest,
        user_obj: CustomUser,
        posts_to_show: str,
) -> int:
    """The function calculates and returns a number of the current page according to parameters in request."""
    post_id = int(request.POST.get('post_id', 0))
    post = get_user_post_by_pk(post_pk=post_id)
    if not post:
        return 1    # if post with given 'pk' does not exist, the function will return the first page number.

    return calculate_post_page(
        paginate_by=USER_POSTS_PAGINATE_BY,
        author_id=user_obj.pk,
        model=UserPost,
        post=post,
        posts_to_show=posts_to_show,
    )


def add_new_params_to_request(request: WSGIRequest, user_obj: CustomUser) -> None:
    # visitors can see only published posts
    posts_to_show = request.POST.get('posts', '') if request.user.pk == user_obj.pk else 'published'
    page = _calculate_post_page_from_user_comment(
        request=request,
        user_obj=user_obj,
        posts_to_show=posts_to_show,
    )
    request.GET._mutable = True
    request.GET['page'] = page
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to the request
        request.GET['posts'] = posts_to_show
