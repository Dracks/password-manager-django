__author__ = 'dracks'

from team_passwords.models import Site, Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    #parent = GroupSerializer
    class Meta:
        model = Group
        fields = ('name', 'parent')

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    group = GroupSerializer
    class Meta:
        model=Site
        fields = ('group', 'name', 'description', 'user', 'password', 'url')
