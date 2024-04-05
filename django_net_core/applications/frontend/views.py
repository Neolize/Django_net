from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View

from applications.user_profiles import forms as up_forms
from applications.user_profiles.permissions import UserPermissionMixin, FORBIDDEN_MESSAGE
from applications.user_profiles.services.crud import (read as up_read, update as up_update,
                                                      create as up_create, delete as up_delete)
from applications.user_profiles.services.utils import form_utils as up_form_utils, common_utils as up_common_utils

from applications.user_wall import forms as uw_forms, models as uw_models
from applications.user_wall.services.crud import create as uw_create, read as uw_read, update as uw_update
from applications.user_wall.services.utils import form_utils as uw_form_utils

from applications.groups import forms as g_forms
from applications.groups import permissions as g_permissions
from applications.groups.services import utils as g_utils
from applications.groups.services.crud import create as g_create, read as g_read, delete as g_delete


class UsersView(ListView):
    template_name = 'user_profiles/list/users.html'
    queryset = up_read.get_all_users()
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class SignupUserView(CreateView):
    template_name = 'account/signup.html'
    form_class = up_forms.SignupUserForm

    def form_valid(self, form: up_forms.SignupUserForm):
        new_user = up_create.create_new_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )
        if new_user:
            login(self.request, user=new_user)
            return redirect(to=new_user)

        form.add_error(None, 'Failed to create a new user. Try one more time.')
        return self.form_invalid(form=form)


class LoginUserView(LoginView):
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
    paginate_by = 1
    form_class = uw_forms.UserCommentForm

    def get(self, request: WSGIRequest, pk: int, form: uw_forms.UserCommentForm | None = None):
        user_obj = up_read.get_user_for_profile(user_pk=pk)
        if not user_obj:
            raise Http404

        context = up_common_utils.form_user_profile_context_data(
            user_obj=user_obj,
            request=self.request,
            paginate_by=self.paginate_by,
        )
        context['form'] = form or self.form_class()
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, pk: int):
        form = self.form_class(request.POST)

        if form.is_valid() and uw_create.create_comment_for_user_post(
            data=form.cleaned_data,
            request=request,
            user_pk=request.user.pk,
        ):
            return self.get(request=request, pk=pk)

        return self.get(request=request, pk=pk, form=form)


def follow_user(request: WSGIRequest, pk: int):
    """Follow a user if the request goes from authenticated and unsubscribed user"""
    if not request.user.is_authenticated:
        return redirect(to='login')

    owner = up_read.get_raw_user_instance(user_pk=pk)
    if not owner:
        raise Http404

    if not up_common_utils.is_followed(current_user=owner, visitor=request.user):
        up_create.create_new_follower(owner=owner, follower=request.user)
    return redirect(to='user_profile', pk=pk)


def unfollow_user(request: WSGIRequest, pk: int):
    if not request.user.is_authenticated:
        return redirect(to='login')

    owner = up_read.get_raw_user_instance(user_pk=pk)
    if not owner:
        raise Http404

    if up_common_utils.is_followed(current_user=owner, visitor=request.user):
        up_delete.delete_follower(owner=owner, follower=request.user)
    return redirect(to='user_profile', pk=pk)


class EditUserProfileView(LoginRequiredMixin, UserPermissionMixin, View):
    template_name = 'user_profiles/detail/edit.html'
    form_class = up_forms.EditUserProfileForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, pk: int):
        form = self.form_class()

        up_form_utils.fill_edit_user_profile_form(
            form=form,
            user_data=up_read.get_user_data_for_edit_profile_view(user_pk=pk),
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
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
        }


class GroupCreationView(LoginRequiredMixin, UserPermissionMixin, View):
    template_name = 'groups/create_group.html'
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
                user_pk=request.user.pk,
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
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
        }


class GroupView(View):
    template_name = 'groups/group.html'

    def get(self, request, group_slug: str):
        group = g_read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        context = {
            'group': group,
            'is_subscribed_to_group': g_utils.is_user_subscribed_to_group(
                group=group,
                visitor=request.user,
            )
        }
        return render(request, self.template_name, context=context)


def follow_group(request: WSGIRequest, group_slug: str):
    """Follow a group if the request goes from authenticated user, who isn't subscribed to this group"""
    if not request.user.is_authenticated:
        return redirect(to='login')

    group = g_read.get_group_by_slug(group_slug)
    if not group:
        raise Http404

    if not g_utils.is_user_subscribed_to_group(group=group, visitor=request.user):
        g_create.create_new_group_follower(group=group, member=request.user)
    return redirect(to='group', group_slug=group_slug)


def unfollow_group(request: WSGIRequest, group_slug: str):
    if not request.user.is_authenticated:
        return redirect(to='login')

    group = g_read.get_group_by_slug(group_slug)
    if not group:
        raise Http404

    if g_utils.is_user_subscribed_to_group(group=group, visitor=request.user):
        g_delete.delete_group_follower(group=group, member=request.user)
    return redirect(to='group', group_slug=group_slug)


class CreateGroupPostView(LoginRequiredMixin, View):
    template_name = 'groups/create_post.html'
    form_class = g_forms.GroupPostForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, group_slug: str):
        group = g_read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        context = {
            'group': group,
            'form': self.form_class(),
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
            'form': form,
        }
        return render(request, self.template_name, context=context)


class UserWallView(LoginRequiredMixin, View):
    template_name = 'user_wall/wall.html'

    def get(self, request: WSGIRequest):
        return render(request, self.template_name)


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
            ),
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
                visitor=request.user,
            ),
        }
        return render(request, self.template_name, context=context)


class PeopleSearchView(View):
    template_name = 'search/people_search.html'

    def get(self, request: WSGIRequest):
        user_input = request.GET.get('input')
        if user_input is None:
            users = up_read.get_all_users_with_personal_data()
        else:
            users = up_read.fetch_users_by_names(user_input)
        context = {
            'users': users,
        }
        return render(request, self.template_name, context=context)


class UserChatView(LoginRequiredMixin, View):
    template_name = 'user_profiles/detail/chat.html'

    def get(self, request, pk):
        return render(request, self.template_name)


class UserChatListView(LoginRequiredMixin, View):
    template_name = 'user_profiles/list/chat_list_second.html'

    def get(self, request):
        return render(request, self.template_name)


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
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
        }


class EditUserPostView(LoginRequiredMixin, View):
    template_name = 'user_wall/edit_post.html'
    form_class = uw_forms.UserPostForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, slug: str):
        user_post = uw_read.get_user_post(slug=slug)
        self.check_request(user_post=user_post)

        context = self.get_context_data(pk=request.user.pk, post_slug=slug)
        uw_form_utils.fill_edit_user_post_form(form=context['form'], post=user_post)
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, slug: str):
        user_post = uw_read.get_user_post(slug=slug)
        self.check_request(user_post=user_post)

        form = self.form_class(request.POST)
        if form.is_valid() and uw_update.update_user_post(data=form.cleaned_data, post=user_post):
            return redirect(to='user_profile', pk=request.user.pk)

        context = self.get_context_data(pk=request.user.pk, post_slug=slug)
        context['form'] = form
        return render(request, self.template_name, context=context)

    def get_context_data(self, pk: int, post_slug: str) -> dict:
        return {
            'form': self.form_class(),
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
            'post_slug': post_slug,
        }

    def check_request(self, user_post: uw_models.UserPost):
        if not user_post:
            raise Http404

        if user_post.author_id != self.request.user.pk:
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)
