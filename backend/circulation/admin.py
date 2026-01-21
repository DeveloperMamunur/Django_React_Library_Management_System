from django.contrib import admin
from .models import Transaction, Reservation, Fine, Payment

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Reservation)
admin.site.register(Fine)
admin.site.register(Payment)