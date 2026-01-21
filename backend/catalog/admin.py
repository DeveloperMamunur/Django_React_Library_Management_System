from django.contrib import admin
from .models import Author, Publisher, Category, Item, Copy


# Register your models here.
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Copy)