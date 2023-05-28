from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View

from applications.user_profiles import forms
from applications.user_profiles.permissions import UserPermissionMixin
from applications.user_profiles.services.crud import read, update, create
from applications.user_profiles.services.utils import form_utils, common_utils


class UsersView(ListView):
    template_name = 'user_profiles/list/users.html'
    queryset = read.get_all_users()
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class SignupUserView(CreateView):
    template_name = 'account/signup.html'
    form_class = forms.SignupUserForm

    def form_valid(self, form: forms.SignupUserForm):
        new_user = create.create_new_user(
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
    form_class = forms.LoginUserForm

    def form_valid(self, form: forms.LoginUserForm):
        create.update_first_login_record(user=form.get_user())
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

    def get(self, request: WSGIRequest, pk: int):
        if not read.is_user_with_given_pk(user_pk=pk):
            raise Http404

        context = {
            'user_obj': common_utils.form_user_data_for_profile_view(
                read.get_user_data_for_profile_view(user_pk=pk)
            ),
        }
        return render(request, self.template_name, context=context)


class EditUserProfileView(LoginRequiredMixin, UserPermissionMixin, View):
    template_name = 'user_profiles/detail/edit.html'
    form_class = forms.EditUserProfileForm
    login_url = reverse_lazy('login')

    def get(self, request: WSGIRequest, pk: int):
        form = self.form_class()
        user_obj = read.get_user_data_for_edit_profile_view(user_pk=pk)

        form_utils.fill_edit_user_profile_form(
            form=form,
            user_data=user_obj,
        )
        context = {
            'form': form,
            'user_obj': common_utils.form_user_data_for_edit_profile_view(user_obj)
        }
        return render(request, self.template_name, context=context)

    def post(self, request: WSGIRequest, pk: int):
        form = self.form_class(request.POST)

        if form.is_valid():
            if update.update_user_profile_data(form=form, user=request.user):
                return redirect(to='edit_user_profile', pk=pk)

        context = {
            'form': form,
            'user_obj': read.get_user_data_for_edit_profile_view(user_pk=pk)
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
