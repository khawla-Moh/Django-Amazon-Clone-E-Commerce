from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Brand,Reviews,ProductImages
from django.db.models import Q,F,Value
from django.db.models.aggregates import Count,Sum,Min,Max,Avg

# Create your views here.






def mydebug(request):
    '''
    ## number column:--------------------------------
    #data=Product.objects.all
    #data=Product.objects.filter(price=20)
    #data=Product.objects.filter(price__gt=98)
    #data=Product.objects.filter(price__gte=98)
    #data=Product.objects.filter(price__lt=98)
    data=Product.objects.filter(price__range=(77,98))
    '''
    
    
    '''
    ## relational query---------------------
    #data=Product.objects.filter(brand__id=5)
    #data=Product.objects.filter(brand__id__gt=200)
    '''

    '''
    ## text query----------------------------
    #data=Product.objects.filter(name__contains='Samantha')
    #data=Product.objects.filter(name__startswith='Samantha')
    #data=Product.objects.filter(name__endswith='thomas')
    #data=Product.objects.filter(tags__isnull=True)
    '''
    
    '''
    ## date:---------------------------------
    #data=Product.objects.filter(date-column-name__year=2022)
    #data=Product.objects.filter(date-column-name__month=12)
    #data=Product.objects.filter(date-column-name__day=2)
    
    '''
    '''
    ##complex queries--------------------------
    #data=Product.objects.filter(flag='New',price__gt=60)
    #data=Product.objects.filter(flag='New').filter(price__gt=60)
    """ data=Product.objects.filter(
    Q(flag='New') |
    Q(price__gt=60)
    )
    """ 
    data=Product.objects.filter(
    ~ Q(flag='New') |
    Q(price__gt=60)
    )
    
    '''
    
    '''
    ##field refernce---------------------------------
    data=Product.objects.filter('quantity=F('price')')
    data=Product.objects.filter('quantity=F('gategory__id')')
    '''

   
    '''
    ##order---------------------------------
    #data=Product.objects.all.order_by('name')  #ASC
    #data=Product.objects.order_by('name')
    #data=Product.objects.order_by('-name')    #DES
    #data=Product.objects.order_by('-name','price')
    #data=Product.objects.filter(price__gt=90).order_by('name')
    #data=Product.objects.order_by('name')[:10]
    #data=Product.objects.earliest('name')
    #data=Product.objects.latest('name')
    ''' 
    '''
    ##limit fields------------------------------
    #data=Product.objects.values('name','price')
    #data=Product.objects.values_list('name','price','brand__name')
    #data=Product.objects.only('name','price')
    data=Product.objects.defer('description','subtitle')
    
    '''
    '''
    ## select related ---------------------------------
    #data=Product.objects.select_related('brand').all()   #foreignkey  one-to-one
    #data=Product.objects.prefetch_related('brand').all()  #            many-to-many    
    
    #data=Product.objects.prefetch_related('category').select_related('brand').all()      
    #data=Product.objects.select_related('category').select_related('brand').all()      

    '''
    '''
    ##aggregation  count Min Max sum avg---------------
    data=Product.objects.aggregate(Avg('price'),Count('id'))
    '''    
    '''
    Annotation-----------------------------------------
    #data=Product.objects.annotate(is_new=Value(0))
    data=Product.objects.annotate(price_with_taxs=F('price')*1.3)
  
    '''
    data=Product.objects.annotate(price_with_taxs=F('price')*1.3)
  
    
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
    queryset=Brand.objects.annotate(product_count=Count('product_prand'))



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
        #context["brand"]=brand=Brand.objects.get(slug=self.kwargs['slug'])
        context["brand"]=brand=Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_prand'))[0]

        return context


""" class BrandDetails(DetailView):
    model=Brand

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context["product"]=Product.objects.filter(brand=self.get_object())
        return context
 """