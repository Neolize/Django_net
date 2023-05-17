from django.http.response import HttpResponse

from applications.user_profiles.services.crud import read


def index(request):
    users = ''.join(user.username for user in read.get_all_users())
    return HttpResponse(f'<h1>Users: {users}</h1>')

