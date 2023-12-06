from django.contrib import admin
from .models import Product,Brand,Reviews,ProductImages
# Register your models here.

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Reviews)
admin.site.register(ProductImages)
