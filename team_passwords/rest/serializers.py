__author__ = 'dracks'

from team_passwords.models import Site, Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    #parent = GroupSerializer
    class Meta:
        model = Group
        fields = ('id', 'name', 'parent')

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Site
        fields = ('id', 'group', 'name', 'description', 'user', 'password', 'url')
