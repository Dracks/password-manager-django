from rest_framework import filters
from team_passwords.models import Group, Site

__author__ = 'dracks'


class SiteGroupFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        group_filter = request.query_params.get('group', None)
        if group_filter is not None:
            group = Group.objects.get(pk=group_filter)
            group_query = group.get_descendants(include_self=True).only('pk')
            list_groups = group_query.iterator()
            list_groups_id = map(lambda e: e.pk, list_groups)
            return queryset.filter(group__in=list_groups_id)
        return queryset

    class Meta:
        model = Site
