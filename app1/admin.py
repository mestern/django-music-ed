from django.contrib import admin
from .models import Post, Ticket
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


# admin.sites.AdminSite.site_header = "پنل مدیریت"
# admin.sites.AdminSite.site_title = "پنل"
# admin.sites.AdminSite.index_title = "مدیریت سایت"

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ('title', 'auther', 'publish', 'status')
    ordering = ('-publish', )
    list_editable = ('status', )
    list_filter = ('auther', ('publish', JDateFieldListFilter), )
    raw_id_fields = ('auther', )


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    pass