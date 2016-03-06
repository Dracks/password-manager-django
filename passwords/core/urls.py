__author__ = 'dracks'

from django.conf.urls import include, url

# from team_passwords.api.resources import SiteResource

from .rest.views import SiteViewSet, GroupViewSet, GroupUserPermissionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sites', SiteViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'group_permissions', GroupUserPermissionViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
