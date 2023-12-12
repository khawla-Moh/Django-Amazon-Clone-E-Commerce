from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Brand,Reviews,ProductImages
# Create your views here.



class ProductList(ListView):
    model =Product





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



class BrandDetails(DetailView):
    pass
