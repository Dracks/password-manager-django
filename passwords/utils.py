from django.contrib.auth.models import User
from rest_framework import serializers

__author__ = 'dracks'

def jwt_response_payload_handler(token, user=None, request=None):
    from passwords.settings import JWT_AUTH

    return {
        'token': token,
        'life_time':JWT_AUTH['JWT_EXPIRATION_DELTA'].total_seconds()
    }