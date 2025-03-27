from django.contrib import admin
from .models import BusinessInquiry

@admin.register(BusinessInquiry)
class BusinessInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_name', 'mobile', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'business_name', 'mobile')

