from django.contrib import admin
from .models import Product,Brand,Reviews,ProductImages
# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
   inlines = [ProductImagesInline,]
   list_display=['name','review_count','flag']



admin.site.register(Product,ProductAdmin)
admin.site.register(Brand)
admin.site.register(Reviews)