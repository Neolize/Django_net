from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View

from applications.user_profiles import forms as up_forms, models as up_models
from applications.user_profiles.permissions import UserPermissionMixin, FORBIDDEN_MESSAGE
from applications.user_profiles.services.crud import read as up_read, update as up_update, create as up_create
from applications.user_profiles.services.utils import form_utils as up_form_utils

from applications.user_wall import forms as uw_forms, models as uw_models
from applications.user_wall.services.crud import create as uw_create, read as uw_read, update as uw_update
from applications.user_wall.services.utils import form_utils as uw_form_utils

from applications.frontend.services.pagination import get_page_object


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

    def get(self, request: WSGIRequest, pk: int):
        user_obj = up_read.get_user_for_profile(user_pk=pk)
        if not user_obj:
            raise Http404

        context = self.get_context_data(user_obj=user_obj, pk=pk)
        return render(request, self.template_name, context=context)

    def get_context_data(self, user_obj: up_models.CustomUser, pk: int) -> dict:
        today = datetime.today()

        page = int(self.request.GET.get('page', 1))
        end = page * self.paginate_by
        start = end - self.paginate_by

        user_posts = uw_read.get_user_posts(user_pk=pk)

        page_obj = get_page_object(
            object_list=user_posts,
            paginate_by=self.paginate_by,
            page=page
        )

        return {
            'user_obj': user_obj,
            'user_posts': user_posts[start:end],
            'today_date': today.date(),
            'yesterday_date': datetime(year=today.year, month=today.month, day=today.day - 1).date(),
            'is_owner': self.request.user.pk == pk,
            'page_obj': page_obj,
        }


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
        context = {
            'form': form,
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
        }
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, pk: int):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid() and up_update.update_user_profile_data(form=form, user=request.user):
            return redirect(to='edit_user_profile', pk=pk)

        context = {
            'form': form,
            'user_obj': up_read.get_user_for_profile(user_pk=pk),
        }
        return render(request, self.template_name, context=context)


class UserWallView(LoginRequiredMixin, View):
    template_name = 'user_wall/wall.html'

    def get(self, request: WSGIRequest):
        return render(request, self.template_name)


class UserFriendsView(LoginRequiredMixin, View):
    template_name = 'user_profiles/list/friends.html'

    def get(self, request: WSGIRequest):
        return render(request, self.template_name)


class UserChatView(LoginRequiredMixin, View):
    template_name = 'user_profiles/detail/chat.html'

    def get(self, request, pk):
        print(f'Current pk: {pk}')
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
