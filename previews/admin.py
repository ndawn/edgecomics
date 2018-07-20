from django.contrib import admin
from previews.models import Preview


@admin.register(Preview)
class PreviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'release_date')
