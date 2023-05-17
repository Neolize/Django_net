from django.shortcuts import render
from django.http import HttpResponse

from applications.user_profiles.services.crud import read


def index(request):
    template = 'user_profiles/list/users.html'
    users = read.get_all_users()[0]
    context = {'title': 'Main page', 'users': users}
    return render(request, template_name=template, context=context)

