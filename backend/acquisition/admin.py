from django.contrib import admin
from .models import Vendor, PurchaseOrder, PurchaseOrderItem

# Register your models here.
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
