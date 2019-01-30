from django.contrib import admin
from explore.communities.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'organizer_name', 'members', 'who']
    list_filter = ['country', 'city']
    search_fields = ['name', 'organizer_name']
    readonly_fields = [f.name for f in Group._meta.fields]
