from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest

from applications.user_profiles import forms
from applications.user_profiles.services.crud import read, update


class UsersView(ListView):
    template_name = 'user_profiles/list/users.html'
    queryset = read.get_all_users()
    context_object_name = 'users'


class SignupUserView(CreateView):
    template_name = 'account/signup.html'
    form_class = forms.SignupUserForm

    def form_valid(self, form: forms.SignupUserForm):
        print("Form valid")
        print(dir(form))
        print(form.cleaned_data)
        return render(self.request, self.template_name, context={'form': self.form_class(self.request.POST)})
        # return redirect(to='signup')
        # return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class LoginUserView(LoginView):
    template_name = 'account/login.html'
    form_class = forms.LoginUserForm

    def form_valid(self, form: forms.LoginUserForm):
        update.update_first_login_record(user=form.get_user())
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

    def get(self, request: WSGIRequest):
        context = {
            'profile_content': 'User profile',
        }
        return render(request, self.template_name, context=context)


class EditUserProfileView(View):
    template_name = 'user_profiles/detail/edit.html'

    def get(self, request: WSGIRequest):
        return render(request, self.template_name)


class UserWallView(View):
    template_name = 'user_wall/wall.html'

    def get(self, request: WSGIRequest):
        return render(request, self.template_name)
