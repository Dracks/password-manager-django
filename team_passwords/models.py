from django.db import models
# from passwords import fields
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

PERMISSION_VALUES = [
    (1, 'Read'),
    (2, 'Write'),
    (3, 'Admin')
]


class Group(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=200)
    access = models.ManyToManyField(User, through='GroupUserPermission', through_fields=('group', 'user'))
    #permissions = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


class GroupUserPermission(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    permission = models.IntegerField(choices=PERMISSION_VALUES)

    class Meta:
        unique_together = ('user', 'group')

    @classmethod
    def get_parent_groups_read(cls, user):
        groups = filter(lambda e: e.permission > 0, GroupUserPermission.objects.filter(user=user))
        groups = map(lambda e: e.group, groups)
        return filter(lambda g: not any(map(lambda e: e in groups, g.get_ancestors())), groups)

    @classmethod
    def get_all_groups_read(cls, user):
        parents = cls.get_parent_groups_read(user)
        list_groups = map(lambda g: g.get_descendants(include_self=True), parents)
        ret = []
        [ret.extend(groups) for groups in list_groups]
        return ret



class Site(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    # password_crypt = fields.EncryptedTextField(blank=True)
    url = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    def group_name(self):
        return self.group.name

    class Meta:
        ordering = ['name']
