from django.contrib import admin
from .models import Member, MembershipType

# Register your models here.
admin.site.register(Member)
admin.site.register(MembershipType)