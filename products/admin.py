from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'price', 'creation_date']
    search_fields = ['name']

admin.site.register(Product,ProductAdmin)