from django.contrib import admin
from webapp.models import Tipe, Tag, Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['name']


class TipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)


admin.site.register(Tipe, TipeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Tag)
