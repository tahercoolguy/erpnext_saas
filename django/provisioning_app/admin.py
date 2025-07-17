from django.contrib import admin
from .models import Company
import base64

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'status', 'created_at', 'get_admin_password')
    readonly_fields = ('get_admin_password',)
    fields = ('name', 'domain', 'status', 'created_at', 'get_admin_password')

    def get_admin_password(self, obj):
        if obj.admin_password:
            try:
                return base64.b64decode(obj.admin_password.encode('utf-8')).decode('utf-8')
            except Exception:
                return '(decode error)'
        return ''
    get_admin_password.short_description = 'Admin Password (decoded)'

admin.site.register(Company, CompanyAdmin)
