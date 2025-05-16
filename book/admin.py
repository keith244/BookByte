from django.contrib import admin
from . models import Book, Bookmark,ReadingProgress
# Register your models here.
admin.site.register(Book)
admin.site.register(Bookmark)
admin.site.register(ReadingProgress)

class BookClubBookInline(admin.TabularInline):
    pass