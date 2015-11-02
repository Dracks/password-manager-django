from django.db import models
# from passwords import fields
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

PERMISSION_VALUES = [
    (1, 'Read'),
    (2, 'Write'),
    (0, 'Admin')
]


class Group(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(User, through='GroupUserPermission', through_fields=('group', 'user'))
    #permissions = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


class GroupUserPermission(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    access = models.IntegerField(choices=PERMISSION_VALUES)

    class Meta:
        unique_together = ('user', 'group')


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
