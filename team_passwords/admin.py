from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin
from .models import Site, Group


class SiteAdmin(admin.ModelAdmin):
    list_display = ('group', 'name', 'description')


class GroupAdmin(MPTTModelAdmin):
    list_display = ('name',)


admin.site.register(Site, SiteAdmin)
admin.site.register(Group, GroupAdmin)
