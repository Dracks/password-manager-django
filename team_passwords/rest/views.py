from rest_framework import filters, status
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
    filter_fields = ('group',)
    search_fields = ('name', 'description')


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        try:
            return viewsets.ModelViewSet.list(self, request, args, kwargs)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        parent = self.request.query_params.get('parent', None)
        show_tree = self.request.query_params.get('show_tree', False)

        if parent is not None:
            obj=Group.objects.get(pk=parent)

            if show_tree:
                return obj.get_descendants()
            else:
                return obj.get_children()
        else:
            if show_tree:
                return Group.objects.all()
            else:
                return Group.objects.filter(parent=None)



class TestView(APIView):
    def get(self, request, format=None):
        snippets = Site.objects.all()
        serializer = SiteSerializer(snippets, many=True)
        return Response(serializer.data)
