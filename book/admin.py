from django.contrib import admin
from . models import Book, Bookmark,ReadingProgress,ReadingSession
from django.utils.html import format_html
# Register your models here.

# admin.site.register(Book)
# admin.site.register(Bookmark)
# admin.site.register(ReadingProgress)

class ReadingProgressInline(admin.TabularInline):
    model = ReadingProgress
    extra = 0

class BookmarkInline (admin.TabularInline):
    model = Bookmark
    extra = 0

class ReadingSessionInline(admin.TabularInline):
    model = ReadingSession
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'user', 'upload_date', 'cover_preview')
    inlines = [ReadingProgressInline, BookmarkInline, ReadingProgressInline]
    def cover_preview (self,obj):
        if obj.cover_pic:
            return format_html(
                "<img src='{}' style='height: 100px' />", obj.cover_pic.url
            )
        return "No Cover pic"
    cover_preview.short_description = 'Cover Preview'

@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'current_page', 'total_pages', 'completed','last_read')
