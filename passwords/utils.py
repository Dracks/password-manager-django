from django.contrib.auth.models import User
from rest_framework import serializers

__author__ = 'dracks'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user':UserSerializer(user).data
    }