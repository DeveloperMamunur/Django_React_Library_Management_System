from django.contrib import admin
from .models import Report, AuditLog

# Register your models here.
admin.site.register(Report)
admin.site.register(AuditLog)