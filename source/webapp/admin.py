from django.contrib import admin
from webapp.models import Tipe, Comment, Tag


class TipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)


admin.site.register(Tipe, TipeAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
