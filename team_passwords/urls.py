__author__ = 'dracks'

from django.conf.urls import include, url

# from team_passwords.api.resources import SiteResource

from team_passwords.rest.views import SiteViewSet, TestView, GroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sites', SiteViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^test/', TestView.as_view())
]
