import datetime

from django.contrib import admin
from .models import *


# from django_jalali.admin.filters import JDateFieldListFilter
# import django_jalali.admin as jadmin


# admin.sites.AdminSite.site_header = "پنل مدیریت"
# admin.sites.AdminSite.site_title = "پنل"
# admin.sites.AdminSite.index_title = "مدیریت سایت"


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    extra = 0


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    inlines = [ImageInlineAdmin, ]
    list_display = ('title', 'auther', 'publish', 'status')
    ordering = ('-publish',)
    list_editable = ('status',)
    list_filter = ('auther', 'publish',)
    raw_id_fields = ('auther',)


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject')


@admin.register(Comment)
class AdminTicket(admin.ModelAdmin):
    list_display = ('name', 'active', 'created')
    list_editable = ['active']

# @admin.register(Image)
# class AdminImage(admin.ModelAdmin):
#     list_display = ["title", 'post', 'created']


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user']