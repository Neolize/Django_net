from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from allauth.account.views import LoginView, SignupView, LogoutView
from allauth.account.forms import LoginForm, SignupForm

from applications.user_profiles import forms
from applications.user_profiles.services.crud import read, update


def index(request):
    template = 'user_profiles/list/users.html'
    users = read.get_all_users()
    context = {'title': 'Main page', 'users': users}
    return render(request, template_name=template, context=context)


class UsersView(ListView):
    template_name = 'user_profiles/list/users.html'
    queryset = read.get_all_users()
    context_object_name = 'users'


class LoginUserView(LoginView):
    # template_name = 'account/login.html'
    # form_class = LoginForm
    def form_valid(self, form: LoginForm):
        print(form.user)
        print(form.user.email)
        print(form.user.first_login)
        print(form.cleaned_data)
        update.update_first_login_record(user=form.user)
        # return super().form_valid(form)
        return redirect(to='login')

    def get_success_url(self):
        return reverse_lazy('home')


class SignupUserView(SignupView):
    form_class = forms.SignupUserForm

    def form_valid(self, form: SignupForm):
        print(dir(form))
        print(form.cleaned_data)
        form.add_error(None, 'This is non fields error')
        return render(self.request, self.template_name, context={'form': form})
        # return redirect(to='signup')

    # def get_authenticated_redirect_url(self):
    #     return reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    def get_redirect_url(self):
        return reverse_lazy('home')
