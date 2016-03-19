from rest_framework import viewsets, views, status
from rest_framework.response import Response
from ...permissions import IsAdminOrReadOnly

from django.contrib.auth.models import User
from .serializers import UserSerializer

def register_endpoints(router):
    router.register('users', UserViewSet)

class MyProfileEndpoint(views.APIView):
    """
    Manage my profile, it requires less permissions to manage that User, but the modifications should be limited

    @todo Limit and control the modifications, (change e-mail or password should require the old password
    """
    resource_name = 'profiles'

    def get_object(self, request):
        return request.user

    def get(self, request, format=None):
        user = self.get_object(request)
        serializer = UserSerializer(user, context={'request': request, 'resource_name': 'profile'})
        return Response(serializer.data)

    def put(self, request, format=None):
        user = self.get_object(request)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        user = self.get_object(request)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_list_query(self):
        current_user = self.request.user
        if current_user.is_staff:
            return User.objects.all()
        else:
            list_groups = current_user.groups.all()
            list_embed_users_id = map(lambda e: e.user_set.values_list('pk', flat=True) ,list_groups)
            list_ids = reduce(lambda ac,e: ac+map(lambda e:e, e), list_embed_users_id, [])
            return User.objects.filter(id__in=list_ids).all()



