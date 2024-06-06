from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404
from django.core.handlers.wsgi import WSGIRequest

from applications.groups import serializers
from applications.groups.services.crud import read


class PublicGroupDetailAPIView(APIView):
    serializer = serializers.PublicGroupDetailSerializer

    def get(self, request: WSGIRequest, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = self.serializer(group)
        return Response(serializer.data)


class PublicGroupListAPIView(APIView):
    serializer = serializers.PublicGroupListSerializer

    def get(self, request: WSGIRequest):
        groups = read.get_all_groups()
        serializer = self.serializer(groups, many=True)
        return Response(serializer.data)


class PublicGroupPostDetailAPIView(APIView):
    serializer = serializers.PublicGroupPostDetailSerializer

    def get(self, request: WSGIRequest, group_post_slug: str):
        post = read.fetch_group_post(group_post_slug)
        if not post:
            raise Http404

        serializer = self.serializer(post)
        return Response(serializer.data)
