from rest_framework import filters
from rest_framework.views import APIView

__author__ = 'dracks'

from team_passwords.models import Site, Group
from team_passwords.rest.serializers import SiteSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_fields = ('group', )
    search_fields = ('name', 'description')

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TestView(APIView):
    def get(self, request, format=None):
        snippets = Site.objects.all()
        serializer = SiteSerializer(snippets, many=True)
        return Response(serializer.data)