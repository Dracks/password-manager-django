from django.db import models
#from passwords.fields import EncryptedCharField

# Create your models here.

class Group(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=200)

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