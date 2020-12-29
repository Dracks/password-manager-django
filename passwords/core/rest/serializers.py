__author__ = 'dracks'

from ..models import Site, Group, GroupUserPermission
from ..permissions import get_group_permissions
from rest_framework import serializers
from django.contrib.auth.models import User


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True)
    children = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    #access = serializers.ManyRelatedField()
    my_permission = serializers.SerializerMethodField(method_name="my_permission_func")

    def my_permission_func(self, obj):
        return get_group_permissions(self.context['request'].user, obj)

    class Meta:
        model = Group
        fields = ('id', 'name', 'parent', 'children', 'my_permission')

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = Site
        fields = ('id', 'group', 'name', 'description', 'user', 'cypher_type', 'password', 'url')

class GroupUserPermissionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = GroupUserPermission
        fields = '__all__'
