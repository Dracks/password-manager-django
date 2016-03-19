__author__ = "dracks"

from django.test import TestCase
from django.contrib.auth.models import User, Group
from passwords.accounts.rest.views import UserViewSet
import mock

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.subject = UserViewSet()
        self.admin = User.objects.create(username="admin")
        self.admin.is_staff = True
        self.user1 = User.objects.create(username="u1")
        self.user2 = User.objects.create(username="u2")
        self.user3 = User.objects.create(username="u3")
        self.user4 = User.objects.create(username="u4")
        self.user5 = User.objects.create(username="u5")

        self.all = Group.objects.create(name="all")
        self.sub1 = Group.objects.create(name="sub1")
        self.sub2 = Group.objects.create(name="sub2")

        self.admin.groups.add(self.all)
        self.user1.groups.add(self.all)
        self.user2.groups.add(self.all)
        self.user3.groups.add(self.all)

        self.user1.groups.add(self.sub1)
        self.user2.groups.add(self.sub1)
        self.user4.groups.add(self.sub1)

        self.user5.groups.add(self.sub2)



    def run_and_check_contains(self, containing_list, step):
        containing_list = map(lambda e: unicode(e), containing_list)
        list_users = self.subject.get_list_query()
        list_usernames = map(lambda e: e.username, list_users)
        self.assertListEqual(list_usernames, containing_list, "Checking step :"+step)


    def test_admin(self):
        self.subject.request = mock.Mock()
        self.subject.request.user = self.admin

        self.run_and_check_contains(["admin", "u1", "u2", "u3", "u4", "u5"], "test-admin")

    def test_all(self):
        self.subject.request = mock.Mock()
        self.subject.request.user = self.user3

        self.run_and_check_contains(["admin", "u1", "u2", "u3"], "test-all")

    def test_sub1(self):
        self.subject.request = mock.Mock()
        self.subject.request.user = self.user4

        self.run_and_check_contains(["u1", "u2", "u4"], "test-sub1")

    def test_alone(self):
        self.subject.request = mock.Mock()
        self.subject.request.user = self.user5

        self.run_and_check_contains(["u5"], "test-alone")



