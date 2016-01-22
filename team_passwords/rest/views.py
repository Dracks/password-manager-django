from rest_framework import filters, status
from team_passwords.filters import SiteGroupFilter

__author__ = 'dracks'

from team_passwords.models import Site, Group, GroupUserPermission
from team_passwords.rest.serializers import SiteSerializer, GroupSerializer, GroupUserPermissionSerializer
from team_passwords.permissions import GroupHasPermissions, SiteHasPermissions, get_group_permissions, \
    GroupUserPermissions
from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.ext.rest_framework import permissions


def check_create_group(field, permission):
    def f(func):
        def func_call(self, request, *args, **kwargs):
            group_pk = request.data[field]
            group_permission = get_group_permissions(request.user, Group.objects.get(pk=group_pk))
            if group_permission >= permission:
                return func(self, request, *args, **kwargs)
            self.permission_denied(request)

        return func_call

    return f

"""
{
    "group": 24,
    "name": "test 1",
    "description": "description",
    "user": "1",
    "password": "1",
    "url": "1"
}
"""

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (SiteHasPermissions,)
    filter_backends = (filters.SearchFilter, SiteGroupFilter)
    filter_class = SiteGroupFilter
    search_fields = ('name', 'description', 'user')

    def get_queryset(self):
        groups = GroupUserPermission.get_all_groups_read(self.request.user)
        return Site.objects.filter(group__in=groups)

    @check_create_group('group', 2)
    def create(self, request, *args, **kwargs):
        return super(SiteViewSet, self).create(request, *args, **kwargs)

    @check_create_group('group', 2)
    def update(self, request, *args, **kwargs):
        return super(SiteViewSet, self).update(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (GroupHasPermissions,)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Group.objects.all()

        return viewsets.ModelViewSet.retrieve(self, request, args, kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_list_queryset()
        try:
            return viewsets.ModelViewSet.list(self, request, args, kwargs)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_list_queryset(self):
        parent = self.request.query_params.get('parent', None)
        show_tree = self.request.query_params.get('show_tree', False)

        if parent is not None and parent != '':
            obj = Group.objects.get(pk=parent)
            permission = get_group_permissions(self.request.user, obj)
            if permission is not None and permission > 0:
                if show_tree:
                    return obj.get_descendants()
                else:
                    return obj.get_children()
            return Group.objects.none()
        else:
            if show_tree:
                return GroupUserPermission.get_all_groups_read(self.request.user)
            else:
                return GroupUserPermission.get_parent_groups_read(self.request.user)

    @check_create_group('parent', 3)
    def create(self, request, *args, **kwargs):
        return super(GroupViewSet, self).create(request, *args, **kwargs)

    @check_create_group('parent', 3)
    def update(self, request, *args, **kwargs):
        return super(GroupViewSet, self).update(request, *args, **kwargs)


class GroupUserPermissionViewSet(viewsets.ModelViewSet):
    queryset = GroupUserPermission.objects.all()
    serializer_class = GroupUserPermissionSerializer
    permission_classes = (GroupUserPermissions, )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('group', 'user')

    @check_create_group('group', 3)
    def create(self, request, *args, **kwargs):
        return super(GroupUserPermissionViewSet, self).create(request, *args, **kwargs)

    @check_create_group('group', 3)
    def update(self, request, *args, **kwargs):
        return super(GroupUserPermissionViewSet, self).update(request, *args, **kwargs)