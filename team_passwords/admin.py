from django.contrib import admin

# Register your models here.
from .models import Site, Group


class SiteAdmin(admin.ModelAdmin):
    list_display = ('group', 'name', 'description')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Site, SiteAdmin)
admin.site.register(Group, GroupAdmin)