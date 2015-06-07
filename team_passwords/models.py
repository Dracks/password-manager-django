from django.db import models
#from passwords.fields import EncryptedCharField
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey


class Group(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Site(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    def group_name(self):
        return self.group.name

    class Meta:
        ordering = ['name']