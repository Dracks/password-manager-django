__author__ = 'dracks'

from team_passwords.models import Site, Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    children = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    class Meta:
        model = Group
        fields = ('id', 'name', 'parent', 'children')

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model=Site
        fields = ('id', 'group', 'name', 'description', 'user', 'password', 'url')
