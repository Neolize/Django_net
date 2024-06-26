from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, View


from django_net_core.settings import USER_POSTS_PAGINATE_BY, GROUP_POSTS_PAGINATE_BY

from applications.frontend import permissions
from applications.frontend.services import utils as f_utils

from applications.abstract_activities.services import utils as aa_utils
from applications.abstract_activities.services.crud import delete as aa_delete

from applications.user_profiles import forms as up_forms, models as up_models
from applications.user_profiles import permissions as up_permissions
from applications.user_profiles.services.crud import (read as up_read, update as up_update,
                                                      create as up_create, delete as up_delete)
from applications.user_profiles.services.utils import form_utils as up_form_utils, common_utils as up_common_utils

from applications.user_wall import forms as uw_forms, models as uw_models
from applications.user_wall.services.utils import (redirect_to_the_current_post_page,
                                                   add_new_params_to_request_from_user_comment)
from applications.user_wall.services.crud import create as uw_create, read as uw_read, update as uw_update

from applications.groups import forms as g_forms, models as g_models, permissions as g_permissions
from applications.groups.services import utils as g_utils
from applications.groups.services.crud import (create as g_create, read as g_read,
                                               delete as g_delete, update as g_update)


class UsersView(ListView):
    template_name = 'user_profiles/list/users.html'
    queryset = up_read.get_all_users()
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class SignupUserView(permissions.UnauthenticatedPermissionsMixin, CreateView):
    template_name = 'account/signup.html'
    form_class = up_forms.SignupUserForm

    def form_valid(self, form: up_forms.SignupUserForm):
        new_user = up_create.create_new_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        if new_user:
            login(self.request, user=new_user)
            return redirect(to=new_user)

        form.add_error(None, 'Failed to create a new user. Try one more time.')
        return self.form_invalid(form=form)


class LoginUserView(permissions.UnauthenticatedPermissionsMixin, LoginView):
    template_name = 'account/login.html'
    form_class = up_forms.LoginUserForm

    def form_valid(self, form: up_forms.LoginUserForm):
        up_create.update_first_login_record(user=form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    template_name = 'account/logout.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def get_redirect_url(self):
        return reverse_lazy('login')


class UserProfileView(View):
    template_name = 'user_profiles/detail/profile.html'
    paginate_by = USER_POSTS_PAGINATE_BY
    form_class = uw_forms.UserCommentForm

    def get(self, request: WSGIRequest, pk: int, form: uw_forms.UserCommentForm | None = None):
        user_obj = up_read.get_user_for_profile(user_pk=pk)
        if not user_obj:
            raise Http404

        context = up_common_utils.form_user_profile_context_data(
            user_obj=user_obj,
            request=request,
            paginate_by=self.paginate_by,
            posts_to_show=request.GET.get('posts', '')
        )
        context['form'] = form or self.form_class()
        return render(request, self.template_name, context=context)


@up_permissions.check_user_request
def handle_user_comment(request: WSGIRequest, pk: int, user_obj: up_models.CustomUser):
    form = uw_forms.UserCommentForm(request.POST)
    is_edited = True if request.POST.get('edit', False) else False

    if request.POST.get('error', None):
        # if an error window was closed, the function will open the same page with a form without any mistakes
        add_new_params_to_request_from_user_comment(request, user_obj)
        # add parameters: page and posts_to_show in order to show user an appropriate page
        return UserProfileView().get(request=request, pk=pk)

    if form.is_valid():
        if is_edited:
            if uw_update.update_user_comment(
                    form=form,
                    request=request
            ):
                return redirect_to_the_current_post_page(request, user_obj)

        elif uw_create.create_comment_for_user_post(
                form=form,
                request=request
        ):
            return redirect_to_the_current_post_page(request, user_obj)

    add_new_params_to_request_from_user_comment(request, user_obj)
    # add parameters: page and posts_to_show in order to show user an appropriate page
    return UserProfileView().get(request=request, pk=pk, form=form)


@up_permissions.check_user_request
def follow_user(request: WSGIRequest, pk: int, owner: up_models.CustomUser):
    """Follow a user if the request goes from authenticated and unsubscribed user."""
    if not up_common_utils.is_followed(current_user=owner, visitor=request.user):
        up_create.create_new_follower(owner=owner, follower=request.user)
    return redirect(to='user_profile', pk=pk)


@up_permissions.check_user_request
def unfollow_user(request: WSGIRequest, pk: int, owner: up_models.CustomUser):
    """Unfollow a user if the request goes from authenticated and subscribed user."""
    if up_common_utils.is_followed(current_user=owner, visitor=request.user):
        up_delete.delete_follower(owner=owner, follower=request.user)
    return redirect(to='user_profile', pk=pk)


class EditUserProfileView(LoginRequiredMixin, up_permissions.UserPermissionMixin, View):
    template_name = 'user_profiles/detail/edit.html'
    form_class = up_forms.EditUserProfileForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, pk: int):
        form = self.form_class()

        up_form_utils.fill_edit_user_profile_form(
            form=form,
            user_data=up_read.get_user_data_for_edit_profile_view(user_pk=pk)
        )
        return render(
            request,
            self.template_name,
            context=self.get_context_data(form, pk)
        )

    def post(self, request: WSGIRequest, pk: int):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid() and up_update.update_user_profile_data(form=form, user=request.user):
            return redirect(to='user_profile', pk=pk)

        return render(
            request,
            self.template_name,
            context=self.get_context_data(form, pk)
        )

    @staticmethod
    def get_context_data(form, pk) -> dict:
        return {
            'form': form,
            'user_obj': up_read.get_user_for_profile(user_pk=pk)
        }


@up_permissions.check_user_request
def delete_user_account(request: WSGIRequest, pk: int, owner: up_models.CustomUser):
    """Delete a user's account if the request goes from the owner of this account"""
    if pk != request.user.pk:
        return HttpResponseForbidden(up_permissions.FORBIDDEN_MESSAGE)

    logout(request)     # log out user before deleting his/her account
    deleted = up_delete.delete_user(owner)
    if not deleted:
        # if an error occurred and a user's account wasn't deleted, the function will log in user backwards
        login(request, user=owner)
    template = 'user_profiles/detail/deleted_profile.html'
    return render(request, template, context={'deleted': deleted})


class CreateUserPostView(LoginRequiredMixin, View):
    template_name = 'user_wall/create_post.html'
    form_class = uw_forms.UserPostForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest):
        return render(request, self.template_name, context=self.get_context_data(pk=request.user.pk))

    def post(self, request: WSGIRequest):
        form = self.form_class(request.POST)

        if form.is_valid() and uw_create.create_user_post_from_form_data(
                data=form.cleaned_data, user_pk=request.user.pk
        ):
            return redirect(to='user_profile', pk=request.user.pk)

        context = self.get_context_data(pk=request.user.pk)
        context['form'] = form
        return render(request, self.template_name, context=context)

    def get_context_data(self, pk: int) -> dict:
        return {
            'form': self.form_class(),
            'user_obj': up_read.get_user_for_profile(user_pk=pk)
        }


class EditUserPostView(LoginRequiredMixin, View):
    template_name = 'user_wall/edit_post.html'
    form_class = uw_forms.UserPostForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, slug: str):
        user_post = uw_read.get_user_post(slug=slug)
        self.check_request(user_post=user_post)

        if not permissions.is_user_post_author(visitor=request.user, post=user_post):
            return HttpResponseForbidden(up_permissions.FORBIDDEN_MESSAGE)

        context = self.get_context_data(pk=request.user.pk, post_slug=slug)
        aa_utils.fill_edit_post_form(form=context['form'], post=user_post)
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, slug: str):
        user_post = uw_read.get_user_post(slug=slug)
        self.check_request(user_post=user_post)

        if not permissions.is_user_post_author(visitor=request.user, post=user_post):
            return HttpResponseForbidden(up_permissions.FORBIDDEN_MESSAGE)

        form = self.form_class(request.POST)
        if form.is_valid() and uw_update.update_user_post(data=form.cleaned_data, post=user_post):
            posts_to_show = request.POST.get('posts', '')

            base_url = reverse('user_profile', kwargs={'pk': request.user.pk})
            page = aa_utils.calculate_post_page(
                paginate_by=USER_POSTS_PAGINATE_BY,
                author_id=user_post.author_id,
                model=uw_models.UserPost,
                post=user_post,
                posts_to_show=posts_to_show
            )
            if posts_to_show:
                # if a parameter 'posts' was given, it'll be added to a new URL
                return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
            return redirect(to=f'{base_url}?page={page}')  # redirect user to an updated post page

        context = self.get_context_data(pk=request.user.pk, post_slug=slug)
        context['form'] = form
        return render(request, self.template_name, context=context)

    def get_context_data(self, pk: int, post_slug: str) -> dict:
        return {
            'form': self.form_class(),
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
            'post_slug': post_slug
        }

    @staticmethod
    def check_request(user_post: uw_models.UserPost):
        if not user_post:
            raise Http404


@up_permissions.check_user_post_deletion_request
def delete_user_post(request: WSGIRequest, user_post: uw_models.UserPost):
    posts_to_show = request.GET.get('posts', '')
    base_url = reverse('user_profile', kwargs={'pk': request.user.pk})
    page = aa_utils.calculate_post_page(
        paginate_by=USER_POSTS_PAGINATE_BY,
        author_id=user_post.author_id,
        model=uw_models.UserPost,
        post=user_post,
        posts_to_show=posts_to_show
    )
    aa_delete.delete_post(user_post)
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')   # redirect user to a new page after a post was deleted


@up_permissions.check_user_comment_deletion_request
def delete_user_comment(request: WSGIRequest, comment: uw_models.UserComment):
    posts_to_show = aa_utils.fetch_posts_to_show_from_previous_url(request)
    page = aa_utils.fetch_page_from_previous_url(request)
    base_url = reverse('user_profile', kwargs={'pk': comment.post.author_id})

    aa_delete.delete_comment(comment)
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')   # redirect user to the same page after his comment was deleted


class UserFollowersView(View):
    template_name = 'user_profiles/list/followers.html'

    def get(self, request: WSGIRequest, pk: int):
        user_obj = up_read.fetch_user_for_followers_page(user_pk=pk)
        if not user_obj:
            raise Http404

        context = {
            'user_obj': user_obj,
            'followers': up_read.fetch_all_user_followers(user_obj),
            'is_followed': up_common_utils.is_followed(
                current_user=user_obj,
                visitor=request.user
            )
        }
        return render(request, self.template_name, context=context)


class UserFollowingView(View):
    template_name = 'user_profiles/list/following.html'

    def get(self, request: WSGIRequest, pk: int):
        user_obj = up_read.fetch_user_for_followers_page(user_pk=pk)
        if not user_obj:
            raise Http404

        context = {
            'user_obj': user_obj,
            'followings': up_read.fetch_all_user_followings(user_obj),
            'is_followed': up_common_utils.is_followed(
                current_user=user_obj,
                visitor=request.user
            )
        }
        return render(request, self.template_name, context=context)


class UserGroupsView(View):
    template_name = 'user_profiles/list/user_groups.html'

    def get(self, request: WSGIRequest, pk: int):
        user_obj = up_read.fetch_user_for_followers_page(user_pk=pk)
        if not user_obj:
            raise Http404

        context = {
            'user_obj': user_obj,
            'groups': g_read.fetch_groups_from_user_obj_for_groups_view(user_obj),
            'is_followed': up_common_utils.is_followed(
                current_user=user_obj,
                visitor=request.user
            )
        }
        return render(request, self.template_name, context=context)


class PeopleSearchView(View):
    template_name = 'search/people_search.html'
    paginate_by = 3

    def get(self, request: WSGIRequest):
        context = f_utils.form_context_data_for_people_search_view(
            request=request,
            paginate_by=self.paginate_by
        )
        return render(request, self.template_name, context=context)


class GroupCreationView(LoginRequiredMixin, up_permissions.UserPermissionMixin, View):
    template_name = 'groups/detail/create_group.html'
    form_class = g_forms.CreateGroup
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, pk: int):
        user_obj = up_read.get_user_for_profile(user_pk=pk)
        if not g_read.is_user_allowed_to_create_group(user_obj):
            return HttpResponseForbidden(g_permissions.GROUP_FORBIDDEN_MESSAGE)

        form = self.form_class()
        context = {
            'form': form,
            'user_obj': user_obj
        }
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, pk: int):
        user_obj = up_read.get_user_for_profile(user_pk=pk)
        if not g_read.is_user_allowed_to_create_group(user_obj):
            return HttpResponseForbidden(g_permissions.GROUP_FORBIDDEN_MESSAGE)

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            new_group = g_create.create_new_group_from_form_data(
                data=form.cleaned_data,
                data_files=request.FILES.dict(),
                user_pk=request.user.pk
            )
            if new_group:
                return redirect(to='group', group_slug=new_group.slug)

        context = {
            'form': form,
            'user_obj': user_obj
        }
        return render(request, self.template_name, context=context)

    @staticmethod
    def get_context_data(form, pk) -> dict:
        return {
            'form': form,
            'user_obj': up_read.get_user_for_profile(user_pk=pk)
        }


class GroupView(View):
    template_name = 'groups/detail/group.html'
    paginate_by = GROUP_POSTS_PAGINATE_BY
    form_class = g_forms.GroupCommentForm

    def get(self, request: WSGIRequest, group_slug: str, form: g_forms.GroupCommentForm | None = None):
        group = g_read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        context = g_utils.form_group_context_data(
            group=group,
            request=request,
            paginate_by=self.paginate_by,
            posts_to_show=request.GET.get('posts', '')
        )
        context['form'] = form or self.form_class()
        return render(request, self.template_name, context=context)


@g_permissions.check_group_request
def handle_group_comment(request: WSGIRequest, group_slug: str, group: g_models.Group):
    form = g_forms.GroupCommentForm(request.POST)

    if request.POST.get('error', None):
        # if an error window was closed, the function will open the same page with a form without any mistakes
        return g_utils.redirect_to_the_current_group_post_page(request, group)

    if form.is_valid():
        if request.POST.get('edit', False):
            if g_update.update_group_comment(
                    form=form,
                    request=request
            ):
                return g_utils.redirect_to_the_current_group_post_page(request, group)

        elif g_create.create_comment_for_group_post(
                form=form,
                request=request
        ):
            return g_utils.redirect_to_the_current_group_post_page(request, group)

    if request.method.lower() == 'get':
        return g_utils.redirect_to_the_current_group_post_page(request, group)

    g_utils.add_new_params_to_request_from_group_comment(request, group)
    # add parameters: page and posts_to_show in order to show user an appropriate page
    return GroupView().get(request=request, group_slug=group_slug, form=form)


@g_permissions.check_group_request
def follow_group(request: WSGIRequest, group_slug: str, group: g_models.Group):
    """Follow a group if the request goes from authenticated user, who isn't subscribed to the group."""
    posts_to_show = aa_utils.fetch_posts_to_show_from_previous_url(request)
    page = aa_utils.fetch_page_from_previous_url(request)
    base_url = reverse('group', kwargs={'group_slug': group_slug})

    if not g_utils.is_user_subscribed_to_group(group=group, visitor=request.user):
        g_create.create_new_group_follower(group=group, member=request.user)

    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')


@g_permissions.check_group_request
def unfollow_group(request: WSGIRequest, group_slug: str, group: g_models.Group):
    """Unfollow a group if the request goes from authenticated user, who is subscribed to the group."""
    posts_to_show = aa_utils.fetch_posts_to_show_from_previous_url(request)
    page = aa_utils.fetch_page_from_previous_url(request)
    base_url = reverse('group', kwargs={'group_slug': group_slug})

    if g_utils.is_user_subscribed_to_group(group=group, visitor=request.user):
        g_delete.delete_group_follower(group=group, member=request.user)

    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')


@g_permissions.check_group_request
def delete_group(request: WSGIRequest, group_slug: str, group: g_models.Group):
    """Delete a group if the request goes from the owner of the group."""
    if group.creator_id != request.user.pk:
        return HttpResponseForbidden(up_permissions.FORBIDDEN_MESSAGE)

    deleted = g_delete.delete_group_instance(group)
    context = {'deleted': deleted}
    if not deleted:
        context['group'] = group
    template = 'groups/detail/deleted_group.html'
    return render(request, template, context=context)


class CreateGroupPostView(LoginRequiredMixin, View):
    template_name = 'groups/detail/create_post.html'
    form_class = g_forms.GroupPostForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, group_slug: str):
        group = g_read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        context = {
            'group': group,
            'form': self.form_class()
        }
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, group_slug: str):
        group = g_read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        if not g_permissions.is_user_group_author(visitor=request.user, group=group):
            return HttpResponseForbidden(g_permissions.GROUP_CREATION_FORBIDDEN_MESSAGE)

        form = self.form_class(request.POST)
        if form.is_valid() and g_create.create_group_post_from_form_data(
            data=form.cleaned_data, user_pk=request.user.pk, group_pk=group.pk
        ):
            return redirect(to='group', group_slug=group_slug)

        context = {
            'group': group,
            'form': form
        }
        return render(request, self.template_name, context=context)


class EditGroupPostView(LoginRequiredMixin, View):
    template_name = 'groups/detail/edit_group_post.html'
    form_class = g_forms.GroupPostForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, group_post_slug: str):
        group_post = g_read.get_group_post_for_editing(group_post_slug)
        if not group_post:
            raise Http404

        if not permissions.is_user_post_author(visitor=request.user, post=group_post):
            return HttpResponseForbidden(up_permissions.FORBIDDEN_MESSAGE)

        context = {
            'form': self.form_class(),
            'group': g_read.get_group_by_slug(group_post.group.slug),
            'group_post_slug': group_post_slug
        }
        aa_utils.fill_edit_post_form(form=context['form'], post=group_post)
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, group_post_slug: str):
        group_post = g_read.get_group_post_for_editing(group_post_slug)
        if not group_post:
            raise Http404

        if not permissions.is_user_post_author(visitor=request.user, post=group_post):
            return HttpResponseForbidden(up_permissions.FORBIDDEN_MESSAGE)

        form = self.form_class(request.POST)
        if form.is_valid() and g_update.update_group_post(data=form.cleaned_data, group_post=group_post):
            posts_to_show = request.POST.get('posts', '')

            base_url = reverse('group', kwargs={'group_slug': group_post.group.slug})
            page = aa_utils.calculate_post_page(
                paginate_by=GROUP_POSTS_PAGINATE_BY,
                author_id=group_post.author_id,
                model=g_models.GroupPost,
                post=group_post,
                posts_to_show=posts_to_show
            )
            if posts_to_show:
                # if a parameter 'posts' was given, it'll be added to a new URL
                return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
            return redirect(to=f'{base_url}?page={page}')  # redirect user to an updated post page

        context = {
            'form': form,
            'group': g_read.get_group_by_slug(group_post.group.slug),
            'group_post_slug': group_post_slug
        }
        return render(request, self.template_name, context=context)


@g_permissions.check_group_post_deletion_request
def delete_group_post(request: WSGIRequest, group_post: g_models.GroupPost):
    """Delete a group post if the request goes from the owner of the post."""
    posts_to_show = request.GET.get('posts', '')
    base_url = reverse('group', kwargs={'group_slug': group_post.group.slug})
    page = aa_utils.calculate_post_page(
        paginate_by=GROUP_POSTS_PAGINATE_BY,
        author_id=group_post.author_id,
        model=g_models.GroupPost,
        post=group_post,
        posts_to_show=posts_to_show
    )
    aa_delete.delete_post(group_post)
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')   # redirect user to a new page after a group post was deleted


@g_permissions.check_group_comment_deletion_request
def delete_group_comment(request: WSGIRequest, comment: g_models.GroupComment):
    posts_to_show = aa_utils.fetch_posts_to_show_from_previous_url(request)
    page = aa_utils.fetch_page_from_previous_url(request)
    base_url = reverse('group', kwargs={'group_slug': comment.post.group.slug})

    aa_delete.delete_comment(comment)
    if posts_to_show:
        # if a parameter 'posts' was given, it'll be added to a new URL
        return redirect(to=f'{base_url}?page={page}&posts={posts_to_show}')
    return redirect(to=f'{base_url}?page={page}')   # redirect user to the same page after his comment was deleted


class GroupFollowersView(View):
    template_name = 'groups/list/group_followers.html'

    def get(self, request: WSGIRequest, group_slug: str):
        group = g_read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        context = {
            'group': group,
            'followers': g_read.fetch_all_group_followers(group),
            'is_subscribed_to_group': g_utils.is_user_subscribed_to_group(
                group=group,
                visitor=request.user
            )
        }
        return render(request, self.template_name, context=context)


class GroupSearchView(View):
    template_name = 'search/group_search.html'
    paginate_by = 3

    def get(self, request: WSGIRequest):
        context = f_utils.form_context_data_for_group_search_view(
            request=request,
            paginate_by=self.paginate_by
        )
        return render(request, self.template_name, context=context)


class UserWallView(LoginRequiredMixin, View):
    template_name = 'user_wall/wall.html'

    def get(self, request: WSGIRequest):
        return render(request, self.template_name)


class UserChatView(LoginRequiredMixin, View):
    template_name = 'user_profiles/detail/chat.html'

    def get(self, request, pk):
        return render(request, self.template_name)


class UserChatListView(LoginRequiredMixin, View):
    template_name = 'user_profiles/list/chat_list_second.html'

    def get(self, request):
        return render(request, self.template_name)


class PostsSearchView(View):
    template_name = 'search/posts_search.html'
    paginate_by = 15
    form_class = uw_forms.UserCommentForm

    def get(self, request: WSGIRequest):
        context = f_utils.form_context_data_for_posts_search_view(
            request=request,
            paginate_by=self.paginate_by
        )
        context['form'] = self.form_class
        return render(request, self.template_name, context=context)
