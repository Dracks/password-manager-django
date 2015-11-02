__author__ = 'dracks'

from rest_framework import permissions

PERMISSIONS_POWER = {
    1: 1,
    2: 2,
    0: 3
}


def get_group_permissions(user, group):
    """
    Get the permissions for a group and this user
    :param group:
    :type group: Group
    :return:
    """
    def reduce_permissions((max_perm, perm), e):
        max_element=PERMISSIONS_POWER[e]
        if max_element>max_perm:
            return (max_element, e)
        else:
            return (max_perm, perm)

    all_permissions = []
    for g in group.get_ancestors(include_self=True):
        all_permissions.extend(g.groupuserpermission_set.filter(user=user))

    return reduce(reduce_permissions, map(lambda e: e.access, all_permissions), (0, None))[1]
