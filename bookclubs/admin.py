from django.contrib import admin
from . models import Comment,BookClub,Membership,BookClubBook
from user.models import User
# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    search_fields = ['email', 'username']


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 1
    # autocomplete_fields = ['user']
    # search_fields = ['user__email', 'user__username']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_club', 'role','joined_at')
    list_filter = ('role', 'book_club')
    search_fields = ('user__username', 'book_club__name')


@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ('name','creator', 'created_at')
    search_fields = ('name', 'creator__username')
    inlines = [MembershipInline]


admin.site.register(Comment)
admin.site.register(BookClubBook)
# admin.site.register(User,UserModelAdmin)