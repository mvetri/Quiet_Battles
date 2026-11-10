from django.contrib import admin

# Register your models here.
from .models import Chapter


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):

    list_display = (
        'chapter_number',
        'title',
        'subtitle',
        'is_published',
        'created_at',
    )

    list_filter = ('is_published',)

    search_fields = ('title', 'subtitle')

    prepopulated_fields = {
        'slug': ('title',)
    }

    list_editable = ('is_published',)

    ordering = ('chapter_number',)