from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin
from .models import Site, Group, GroupUserPermission


class SiteAdmin(admin.ModelAdmin):
    list_display = ('group', 'name', 'description')


class GroupUserPermissionInline(admin.StackedInline):
    model = GroupUserPermission
    extra = 1


class GroupAdmin(MPTTModelAdmin):
    list_display = ('name',)
    inlines = [GroupUserPermissionInline]


admin.site.register(Site, SiteAdmin)
admin.site.register(Group, GroupAdmin)
