from django.contrib import admin

from .models import Lead,Webscraping

#admin.site.register(Lead)
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'country','city','address','website','created_at')
    list_filter = ('created_at', 'company_name')
    search_fields = ('company_name', 'email', 'message')
    date_hierarchy = 'created_at'
    ordering = ('created_at',) 
admin.site.register(Webscraping)

