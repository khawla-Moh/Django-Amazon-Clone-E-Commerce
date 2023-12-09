from collections.abc import Iterable
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
FLAG_TYPE=(

    ('New','New'),
    ('Sale','Sale'),
    ('Feature','Feature')
)

# Create your models here.
class Product(models.Model):
    name=models.CharField(_('name'),max_length= 150)
    flag=models.CharField(_('flag'),max_length=15,choices=FLAG_TYPE)
    price=models.FloatField(_('price'))
    image=models.ImageField(_('image'),upload_to='product')
    sku=models.IntegerField(_('sku'))
    subtitle=models.TextField(_('subtitle'),max_length=400)
    description=models.TextField(_('description'),max_length=20000)
    tags = TaggableManager() 
    brand=models.ForeignKey('Brand',verbose_name=_('brand'),related_name='product_prand',on_delete=models.SET_NULL,null=True)
  
    slug=models.SlugField(blank=True,null=True)
    
    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class ProductImages(models.Model):
    Product=models.ForeignKey(Product,verbose_name=_('product'),related_name='product_images',on_delete=models.CASCADE)
    image=models.ImageField(_('image'),upload_to='productimages')



class Reviews(models.Model):
    user=models.ForeignKey(User,verbose_name=_('user'),related_name='reviews_user',on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,verbose_name=_('product'),related_name='reviews_product',on_delete=models.CASCADE)
    review=models.TextField(_('review'),max_length=700)
    date=models.DateTimeField(_('date'),default=timezone.now)
    rate=models.IntegerField(_('rate'),choices=[(i,i) for i  in range(1,6)])

    
    def __str__(self):
        return f'{self.user}-{self.review}-{self.rate}'



class Brand(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='brand')
    slug=models.SlugField(blank=True,null=True)
    
    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

