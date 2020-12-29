from .models import GroupUserPermission

__author__ = 'dracks'

from rest_framework import permissions


def get_group_permissions(user, group):
    """
    Get the permissions for a group and this user
    :param group:
    :type group: Group
    :return:
    """

    all_permissions = []
    for g in group.get_ancestors(include_self=True):
        all_permissions.extend(g.groupuserpermission_set.filter(user=user))
    max_permissions = 0
    for w in map(lambda e: e.permission, all_permissions):
        max_permissions=max(w, max_permissions)

    return max_permissions


class GroupHasPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        permission = get_group_permissions(request.user, obj)
        if request.method in permissions.SAFE_METHODS:
            if permission is not None and permission >= 1:
                return True
            else:
                list_parents = GroupUserPermission.get_parent_groups_read(request.user)
                descendant = obj.get_descendants()
                return any(map(lambda d: d in list_parents, descendant))

                # Write permissions are only allowed to the owner of the snippet.
        return permission is not None and permission >= 3


class SiteHasPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        permission = get_group_permissions(request.user, obj.group)
        if request.method in permissions.SAFE_METHODS:
            return permission is not None and permission >= 1

            # Write permissions are only allowed to the owner of the snippet.
        return permission is not None and permission >= 2

class GroupUserPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        permission = get_group_permissions(request.user, obj.group)
        if request.method in permissions.SAFE_METHODS:
            return permission is not None and permission >=2

        return permission is not None and permission >= 3
