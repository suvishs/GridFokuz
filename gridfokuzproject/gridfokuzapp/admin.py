from django.contrib import admin
from .models import AddVendors, AddProducts

# Register your models here.

admin.site.register(AddVendors)
admin.site.register(AddProducts)