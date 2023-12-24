from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Brand,Reviews,ProductImages
# Create your views here.






def mydebug(request):
    data=Product.objects.all
    return render(request,'products/debug.html',{'data':data})





class ProductList(ListView):
    model =Product
    paginate_by=50

#context{},queryset: Product.objexts.all() : 1 : option  2:method :override
#queryset :main query [detail product]
#context:extra data   [reviews,images]

class ProductDetail(DetailView):
    model=Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewsTem']=Reviews.objects.filter(product=self.get_object())
        context['images']=ProductImages.objects.filter(Product=self.get_object())
        context['related']=Product.objects.filter(brand=self.get_object().brand)
        return context
    

class BrandList(ListView):
    model=Brand
    paginate_by=50



class BrandDetails(ListView):
    model=Product
    template_name='products/brand_detail.html'
    paginate_by=30

    def get_queryset(self):
        brand=Brand.objects.get(slug=self.kwargs['slug'])
        queryset=super().get_queryset().filter(brand=brand)
        return queryset

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context["brand"]=brand=Brand.objects.get(slug=self.kwargs['slug'])

        return context


""" class BrandDetails(DetailView):
    model=Brand

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context["product"]=Product.objects.filter(brand=self.get_object())
        return context
 """