from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404
from django.core.handlers.wsgi import WSGIRequest

from applications.user_profiles import serializers
from applications.user_profiles.services.crud import read


class PublicUserDetailAPIView(APIView):
    serializer = serializers.PublicUserDetailSerializer

    def get(self, request: WSGIRequest, pk: int):
        user = read.get_user_by_pk(pk)
        if not user:
            raise Http404

        serializer = self.serializer(user)
        return Response(serializer.data)


class PublicUserListAPIView(APIView):
    serializer = serializers.PublicUserListSerializer

    def get(self, request: WSGIRequest):
        users = read.get_all_users()
        serializer = self.serializer(users, many=True)
        return Response(serializer.data)
