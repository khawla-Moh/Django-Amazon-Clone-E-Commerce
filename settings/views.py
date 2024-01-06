from django.shortcuts import render
from django.db.models.aggregates import Count
from products.models import Product,Brand,Reviews



# Create your views here.
def home(request):
    new_product=Product.objects.filter(flag='New')[:10]
    sale_product=Product.objects.filter(flag='Sale')
    feature_product=Product.objects.filter(flag='Feature')
    brand=Brand.objects.annotate(product_count=Count('product_prand'))
    reviews=Reviews.objects.all





    return render(request,'settings/home.html',{
        'new_product':new_product,
        'sale_product':sale_product,
        'feature_product':feature_product,
        'brand':brand,
        'reviews':reviews
    })