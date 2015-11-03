__author__ = 'dracks'

from django.test import TestCase
from django.contrib.auth.models import User
from team_passwords import models
from team_passwords import permissions

class PermissionsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="u1")
        self.user2 = User.objects.create(username="u2")
        self.group1 = models.Group.objects.create()
        self.group2 = models.Group.objects.create(parent=self.group1)
        self.group3 = models.Group.objects.create(parent=self.group2)
        self.group4 = models.Group.objects.create()
        models.GroupUserPermission.objects.create(user=self.user1, group=self.group1, permission=1)
        models.GroupUserPermission.objects.create(user=self.user1, group=self.group3, permission=2)
        models.GroupUserPermission.objects.create(user=self.user2, group=self.group3, permission=0)


    def test_self(self):
        self.assertEqual(permissions.get_group_permissions(self.user1, self.group1), 1)
        self.assertEqual(permissions.get_group_permissions(self.user1, self.group3), 2)
        self.assertEqual(permissions.get_group_permissions(self.user2, self.group3), 0)

    def test_ancestors(self):
        self.assertEqual(permissions.get_group_permissions(self.user1, self.group2), 1)
        self.assertEqual(permissions.get_group_permissions(self.user2, self.group2), None)
        self.assertEqual(permissions.get_group_permissions(self.user1, self.group4), None)
