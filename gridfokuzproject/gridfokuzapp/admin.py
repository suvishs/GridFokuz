from django.contrib import admin
from .models import AddVendors, AddProducts, ManualComboTemp, Logo

# Register your models here.

admin.site.register(AddVendors)
admin.site.register(AddProducts)
admin.site.register(ManualComboTemp)
admin.site.register(Logo)